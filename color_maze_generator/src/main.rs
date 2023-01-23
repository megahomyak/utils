use std::ops::Add;

// Must contain at least 3 elements for the algorithm to work properly, and this is also the
// recommended amount.
const MARKS: &'static [&'static str] = &[":PhiClueless:", ":PhiEmbarrassed:", ":PhiThreaten:"];
const DESIRED_DISTANCE: u32 = 40;
const MAZE_WIDTH: usize = 10;
const MAZE_HEIGHT: usize = 10;

fn get_mark_index(distance: Distance) -> usize {
    usize::try_from(distance.0 % u32::try_from(MARKS.len()).unwrap()).unwrap()
}

fn get_mark(distance: Distance) -> &'static str {
    MARKS[get_mark_index(distance)]
}

#[derive(Clone, Debug)]
struct Matrix<const Width: usize, const Height: usize, T> {
    contents: [[T; Width]; Height],
}

impl<const Width: usize, const Height: usize, T> Matrix<Width, Height, T> {
    pub fn new(filler: T) -> Self
    where
        T: Copy,
    {
        Self {
            contents: [[filler; Width]; Height],
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

type Maze = Matrix<MAZE_WIDTH, MAZE_HEIGHT, Option<Distance>>;

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

fn make_a_maze(mut state: State) -> Option<Maze> {
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
    let self_distance = match state.maze.get_mut(state.position.x, state.position.y) {
        Some(cell @ None) => cell,
        _ => return None, // We're either out of bounds or the cell is already taken.
    };
    *self_distance = Some(state.distance);
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
    for (position, _distance) in adjacent(&state.maze, state.position.x, state.position.y) {
        let new_state = State {
            maze: state.maze.clone(),
            position,
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
    }).unwrap();
    for line in maze.contents {
        for cell in line {
            print!("{} ", cell.map(|distance| get_mark(distance)).unwrap_or(":popgoes2:"))
        }
        print!("\n");
    }
}
