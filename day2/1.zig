const std = @import("std");
const file = @embedFile("input2.txt");

const split = std.mem.split;
const allocator = std.heap.page_allocator;
const whitespace = " \t\n\r";

const CubeValues = struct {
    red: u32,
    green: u32,
    blue: u32,
};

const Color = enum {
    red,
    green,
    blue,
};

const GameRecord = struct {
    values: std.ArrayList(CubeValues),
};

fn stringToColor(s: []const u8) ?Color {
    if (std.mem.eql(u8, s, "red")) {
        return Color.red;
    } else if (std.mem.eql(u8, s, "green")) {
        return Color.green;
    } else if (std.mem.eql(u8, s, "blue")) {
        return Color.blue;
    } else {
        return null;
    }
}

fn setColor(s: *CubeValues, color: Color, value: u8) void {
    switch (color) {
        .red => s.red = value,
        .green => s.green = value,
        .blue => s.blue = value,
    }
}

fn parseGameLine(line: []const u8) !GameRecord {
    var line_split = split(u8, line, ": ");
    _ = (line_split.next() orelse return error.MissingKey)[0..];
    const raw_values = (line_split.next() orelse return error.MissingValues)[0..];

    var values = std.ArrayList(CubeValues).init(allocator);

    var game_split = split(u8, raw_values, "; ");
    while (game_split.next()) |game_value| {
        var colors_list = split(u8, game_value, ", ");

        var cube_values = CubeValues{ .red = 0, .green = 0, .blue = 0 };

        while (colors_list.next()) |game| {
            const trimmed_color = std.mem.trim(u8, game, whitespace);
            var game_values = split(u8, trimmed_color, " ");
            const number: u8 = try std.fmt.parseInt(u8, game_values.next().?, 10);
            const color = (game_values.next() orelse return error.MissingKey)[0..];
            const field = stringToColor(color) orelse return error.MissingKey;

            setColor(&cube_values, field, number);
        }
        try values.append(cube_values);
    }

    return GameRecord{
        .values = values,
    };
}

pub fn main() !void {
    var total: u32 = 0;
    var counter: u32 = 1;
    var splits = split(u8, file, "\n");
    const limits = CubeValues{
        .red = 12,
        .green = 13,
        .blue = 14,
    };

    while (splits.next()) |line| {
        const game_line = parseGameLine(line) catch break;
        var count_game_line = true;
        for (game_line.values.items) |cubes| {
            if (limits.red < cubes.red or limits.green < cubes.green or limits.blue < cubes.blue) {
                count_game_line = false;
            }
        }
        if (count_game_line) {
            total += counter;
        }

        counter += 1;
    }

    std.debug.print("Total: {d}\n", .{total});
}
