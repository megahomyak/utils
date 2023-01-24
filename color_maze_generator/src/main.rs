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

fn get_mark_index(distance: Distance) -> usize {
    usize::try_from(distance.0 % u32::try_from(MARKS.len()).unwrap()).unwrap()
}

fn get_mark(distance: Distance) -> &'static str {
    MARKS[get_mark_index(distance)]
}

#[derive(Clone, Debug)]
struct Matrix<const WIDTH: usize, const HEIGHT: usize, T> {
    contents: [[T; WIDTH]; HEIGHT],
}

type Maze = Matrix<MAZE_WIDTH, MAZE_HEIGHT, Option<Distance>>;

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
) -> impl Iterator<Item = (Position, &Option<Distance>)> {
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
    for line in maze.contents {
        for cell in line {
            print!(
                "{}",
                cell.map(|distance| get_mark(distance))
                    .unwrap_or(":popgoes2:")
            )
        }
        print!("\n");
    }
}

fn print_mark_indexes(maze: &Maze) {
    for line in maze.contents {
        for cell in line {
            match cell {
                None => print!(" "),
                Some(distance) => print!("{}", get_mark_index(distance)),
            }
        }
        print!("\n");
    }
}

fn make_a_maze(mut state: State) -> Option<Maze> {
    let self_distance = match state.maze.get_mut(state.position.x, state.position.y) {
        Some(cell @ None) => cell,
        _ => return None, // We're either out of bounds or the cell is already taken.
    };
    *self_distance = Some(state.distance);
    if state.position
        == (Position {
            x: MAZE_WIDTH - 1,
            y: MAZE_HEIGHT - 1,
        })
    {
        if state.distance.0 >= DESIRED_DISTANCE {
            for cell in state.maze.contents.iter_mut() {
                
            }
            return Some(state.maze);
        } else {
            return None;
        }
    }
    for (_position, distance) in adjacent(&state.maze, state.position.x, state.position.y)
        .filter_map(|cell| {
            if let (pos, Some(distance)) = cell {
                Some((pos, distance))
            } else {
                None
            }
        })
    {
        if get_mark_index(state.distance + 1) == get_mark_index(*distance) {
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
            if let maze @ Some(_) = make_a_maze(new_state) {
                return maze;
            }
        }
        let new_state = State {
            maze: state.maze,
            position: first_position,
            distance: state.distance + 1,
        };
        if let maze @ Some(_) = make_a_maze(new_state) {
            return maze;
        }
    }
    None
}

fn main() {
    let maze = make_a_maze(State {
        distance: Distance(0),
        position: Position { x: 0, y: 0 },
        maze: Matrix::new(None),
    })
    .expect("A maze of such size with such path length cannot be built!");
    print_the_maze(&maze);
}
