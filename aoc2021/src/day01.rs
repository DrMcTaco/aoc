#[aoc(day1, part1)]
pub fn solve_part1(input: &str) -> u32 {
    let mut incr = 0;

    let nums = input
        .lines()
        .map(|l| l.parse().unwrap())
        .collect::<Vec<u32>>();

    for i in 0..nums.iter().count() - 1 {
        if nums[i] < nums[i + 1] {
            incr += 1
        }
    }
    incr
}

#[aoc(day1, part2)]
pub fn solve_part2(input: &str) -> u32 {
    let mut incr = 0;

    let nums = input
        .lines()
        .map(|l| l.parse().unwrap())
        .collect::<Vec<u32>>();

    for i in 0..nums.iter().count() - 3 {
        if nums[i] + nums[i + 1] + nums[i + 2] < nums[i + 1] + nums[i + 2] + nums[i + 3] {
            incr += 1
        }
    }

    incr
}
