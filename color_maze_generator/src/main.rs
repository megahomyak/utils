use std::ops::Add;

use rand::{seq::SliceRandom, thread_rng};

// Must contain at least 3 elements for the algorithm to work properly, and this is also the
// recommended amount.
const MARKS: &'static [&'static str] = &[":PhiClueless:", ":PhiEmbarrassed:", ":PhiThreaten:"];
const DESIRED_DISTANCE: u32 = 40;
const MAZE_WIDTH: usize = 10;
const MAZE_HEIGHT: usize = 10;
const BEGINNING_MARK: &'static str = ":HandPointDown:";
const END_MARK: &'static str = ":HandPointRight:";
const EMPTY_SPOT: &'static str = ":popgoes2:";

fn join<T: AsRef<str>, I: Iterator<Item = T>>(mut i: I, separator: &str) -> String {
    let mut s = String::new();
    if let Some(contents) = i.next() {
        s.push_str(contents.as_ref());
        for contents in i {
            s.push_str(separator);
            s.push_str(contents.as_ref());
        }
    }
    s
}

fn get_mark_index(distance: Distance) -> usize {
    usize::try_from(distance.0 % u32::try_from(MARKS.len()).unwrap()).unwrap()
}

fn get_next_mark_index(mark_index: MarkIndex) -> MarkIndex {
    (mark_index + 1) % MARKS.len()
}

#[derive(Clone, Debug)]
struct Matrix<const WIDTH: usize, const HEIGHT: usize, T> {
    contents: [[T; WIDTH]; HEIGHT],
}

type MarkIndex = usize;
type Maze = Matrix<MAZE_WIDTH, MAZE_HEIGHT, Option<MarkIndex>>;

impl<const WIDTH: usize, const HEIGHT: usize, T> Matrix<WIDTH, HEIGHT, T> {
    pub fn new(filler: T) -> Self
    where
        T: Copy,
    {
        Self {
            contents: [[filler; WIDTH]; HEIGHT],
        }
    }

    pub fn get(&self, x: usize, y: usize) -> Option<&T> {
        self.contents.get(y).and_then(|row| row.get(x))
    }

    pub fn get_mut(&mut self, x: usize, y: usize) -> Option<&mut T> {
        self.contents.get_mut(y).and_then(|row| row.get_mut(x))
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct Position {
    pub x: usize,
    pub y: usize,
}

#[derive(Clone, Copy, Debug)]
struct Distance(pub u32);

impl Add<u32> for Distance {
    type Output = Self;

    fn add(self, rhs: u32) -> Self::Output {
        Self(self.0.checked_add(rhs).unwrap())
    }
}

fn adjacent(
    maze: &Maze,
    x: usize,
    y: usize,
) -> impl Iterator<Item = (Position, &Option<MarkIndex>)> {
    [(-1, 0), (1, 0), (0, 1), (0, -1)]
        .into_iter()
        .filter_map(move |(x_bias, y_bias)| {
            x.checked_add_signed(x_bias)
                .zip(y.checked_add_signed(y_bias))
        })
        .filter_map(|(x, y)| maze.get(x, y).map(|distance| (Position { x, y }, distance)))
}

#[derive(Debug)]
struct State {
    pub maze: Maze,
    pub position: Position,
    pub distance: Distance,
}

fn print_the_maze(maze: &Maze) {
    print!(
        "{}",
        join(
            maze.contents.iter().map(|row| {
                row.iter()
                    .map(|cell| {
                        cell.map(|mark_index| MARKS[mark_index])
                            .unwrap_or(EMPTY_SPOT)
                    })
                    .collect::<String>()
            }),
            &"\n".to_owned()
        )
    );
}

fn print_mark_indexes(maze: &Maze) {
    for line in maze.contents {
        for cell in line {
            match cell {
                None => print!(" "),
                Some(mark_index) => print!("{}", MARKS[mark_index]),
            }
        }
        print!("\n");
    }
}

fn finish_the_maze(maze: &mut Maze) {
    for x in 0..MAZE_WIDTH {
        for y in 0..MAZE_HEIGHT {
            let None = maze.get(x, y).unwrap() else { continue; };
            let mut current_distance = None;
            let mut mark_indexes: Vec<_> = (0..MARKS.len()).collect();
            mark_indexes.shuffle(&mut thread_rng());
            for current_cell_mark_index in mark_indexes {
                if adjacent(&maze, x, y).all(
                    |(_adjacent_cell_positions, adjacent_cell_distance)| {
                        // An adjacent cell is either not filled or we cannot go on it from the
                        // current cell
                        adjacent_cell_distance.map_or(true, |adjacent_cell_mark_index| {
                            adjacent_cell_mark_index != get_next_mark_index(current_cell_mark_index)
                        })
                    },
                ) {
                    current_distance = Some(current_cell_mark_index);
                    break;
                }
            }
            *maze.get_mut(x, y).unwrap() = current_distance;
        }
    }
}

fn make_the_right_path(mut state: State) -> Option<Maze> {
    let Some(self_distance @ None) = state.maze.get_mut(state.position.x, state.position.y) else {
        return None; // We're either out of bounds or the cell is already taken.
    };
    *self_distance = Some(get_mark_index(state.distance));
    if state.position
        == (Position {
            x: MAZE_WIDTH - 1,
            y: MAZE_HEIGHT - 1,
        })
    {
        if state.distance.0 >= DESIRED_DISTANCE {
            return Some(state.maze);
        } else {
            return None;
        }
    }
    for (_position, mark_index) in adjacent(&state.maze, state.position.x, state.position.y)
        .filter_map(|cell| {
            if let (pos, Some(distance)) = cell {
                Some((pos, distance))
            } else {
                None
            }
        })
    {
        if get_mark_index(state.distance + 1) == *mark_index {
            return None; // One of the adjacent cells can be accessed from the current one.
        }
    }
    let mut adjacent: Vec<_> = adjacent(&state.maze, state.position.x, state.position.y).collect();
    adjacent.shuffle(&mut thread_rng());
    let mut adjacent = adjacent.into_iter();
    if let Some((first_position, _first_distance)) = adjacent.next() {
        for (position, _distance) in adjacent {
            let new_state = State {
                maze: state.maze.clone(),
                position,
                distance: state.distance + 1,
            };
            if let maze @ Some(_) = make_the_right_path(new_state) {
                return maze;
            }
        }
        let new_state = State {
            maze: state.maze,
            position: first_position,
            distance: state.distance + 1,
        };
        if let maze @ Some(_) = make_the_right_path(new_state) {
            return maze;
        }
    }
    None
}

fn main() {
    let mut maze = make_the_right_path(State {
        distance: Distance(0),
        position: Position { x: 0, y: 0 },
        maze: Matrix::new(None),
    })
    .expect("A maze of such size with such path length cannot be built!");
    println!("Solution:");
    print_the_maze(&maze);
    print!("\n\n");
    finish_the_maze(&mut maze);
    println!(
        "Rules: get from {BEGINNING_MARK} to {END_MARK} by following the cells in this order: {}",
        join(MARKS.iter(), ", ")
    );
    println!("{}", BEGINNING_MARK);
    print_the_maze(&maze);
    println!("{}", END_MARK);
}
