const std = @import("std");
const file = @embedFile("sample.txt");

const split = std.mem.split;
const allocator = std.heap.page_allocator;
const whitespace = " \t\n\r";

const CubeValues = struct {
    red: []const u8,
    green: []const u8,
    blue: []const u8,
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

fn setColor(s: *CubeValues, color: Color, value: []const u8) void {
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

    var values = std.ArrayList(CubeValues).init(allocator); // Dereference the pointer here

    var game_split = split(u8, raw_values, "; ");
    while (game_split.next()) |game_value| {
        var colors_list = split(u8, game_value, ", ");
        var cube_values = CubeValues{ .red = "0", .green = "0", .blue = "0" };

        while (colors_list.next()) |game| {
            const trimmed_color = std.mem.trim(u8, game, whitespace);
            var game_values = split(u8, trimmed_color, " ");

            const number = (game_values.next() orelse return error.MissingValues)[0..];
            const color = (game_values.next() orelse return error.MissingKey)[0..];
            const field = stringToColor(color) orelse return error.MissingKey;

            setColor(&cube_values, field, number);
        }
        std.debug.print("red: {s}, green: {s}, blue: {s} \n", .{ cube_values.red, cube_values.green, cube_values.blue });
        try values.append(cube_values);
    }

    return GameRecord{
        .values = values,
    };
}

pub fn main() !void {
    var total: u8 = 0;
    var counter: u8 = 1;
    var splits = split(u8, file, "\n");
    while (splits.next()) |line| {
        _ = try parseGameLine(line);
        //std.debug.print("Values: {s}\n", .{record.values.items});
        total += 1;
        counter += 1;
        std.debug.print("Counter: {d}, Total: {d} \n", .{ counter, total });
    }

    std.debug.print("{d}", .{total});
}
