`timescale 1ns/1ps
`default_nettype none

module tb_combolock;

    reg  [7:0] ui_in;
    wire [7:0] uo_out;
    reg  [7:0] uio_in;
    wire [7:0] uio_out;
    wire [7:0] uio_oe;
    reg        ena;
    reg        clk;
    reg        rst_n;

    reg       key_is_down;
    reg [1:0] pressed_row;
    reg [1:0] pressed_col;

    tt_um_combolock dut (
        .ui_in(ui_in),
        .uo_out(uo_out),
        .uio_in(uio_in),
        .uio_out(uio_out),
        .uio_oe(uio_oe),
        .ena(ena),
        .clk(clk),
        .rst_n(rst_n)
    );

    always #5 clk = ~clk;

    always @* begin
        uio_in = 8'hf0;
        if (key_is_down && !uio_out[pressed_row]) begin
            uio_in[7:4] = ~(4'b0001 << pressed_col);
        end
    end

    task check_output;
        input [7:0] value;
        input [255:0] message;
        begin
            if (uo_out !== value) begin
                $display("FAIL: %0s expected=%b got=%b", message, value, uo_out);
                $finish;
            end
        end
    endtask

    task press_key;
        input [1:0] row;
        input [1:0] col;
        begin
            @(negedge clk);
            pressed_row = row;
            pressed_col = col;
            key_is_down = 1'b1;
            repeat (8) @(negedge clk);
            key_is_down = 1'b0;
            repeat (8) @(negedge clk);
        end
    endtask

    task press_code;
        input [3:0] code;
        begin
            case (code)
                4'h1: press_key(2'd0, 2'd0);
                4'h2: press_key(2'd0, 2'd1);
                4'h3: press_key(2'd0, 2'd2);
                4'ha: press_key(2'd0, 2'd3);
                4'h4: press_key(2'd1, 2'd0);
                4'h5: press_key(2'd1, 2'd1);
                4'h6: press_key(2'd1, 2'd2);
                4'hb: press_key(2'd1, 2'd3);
                4'h7: press_key(2'd2, 2'd0);
                4'h8: press_key(2'd2, 2'd1);
                4'h9: press_key(2'd2, 2'd2);
                4'hc: press_key(2'd2, 2'd3);
                4'h0: press_key(2'd3, 2'd1);
                4'hd: press_key(2'd3, 2'd3);
                default: begin
                    $display("FAIL: unsupported code key %h", code);
                    $finish;
                end
            endcase
        end
    endtask

    task press_star;
        begin
            press_key(2'd3, 2'd0);
        end
    endtask

    task press_hash;
        begin
            press_key(2'd3, 2'd2);
        end
    endtask

    task set_password;
        input [3:0] code;
        begin
            press_code(code);
            press_star();
        end
    endtask

    task enter_code;
        input [3:0] code;
        begin
            press_code(code);
            press_hash();
        end
    endtask

    initial begin
        $dumpfile("sim/tb_combolock.vcd");
        $dumpvars(0, tb_combolock);

        ui_in        = 8'h00;
        key_is_down  = 1'b0;
        pressed_row  = 2'd0;
        pressed_col  = 2'd0;
        ena          = 1'b1;
        clk          = 1'b0;
        rst_n        = 1'b0;

        repeat (2) @(negedge clk);
        rst_n = 1'b1;
        repeat (2) @(negedge clk);

        // Reset: default password is 0, no attempts, locked output is low.
        check_output(8'b0000_0000, "reset state");
        if (uio_oe !== 8'b0000_1111) begin
            $display("FAIL: uio_oe expected=00001111 got=%b", uio_oe);
            $finish;
        end

        // DIP-style code entry on ui_in is ignored.
        @(negedge clk);
        ui_in = {2'b00, 1'b1, 1'b0, 4'ha};
        repeat (4) @(negedge clk);
        ui_in = 8'h00;
        check_output(8'b0000_0000, "ui_in code entry ignored");

        // Change password to 1010 using A, then *.
        set_password(4'ha);
        check_output(8'b1010_0000, "password changed");

        // Correct password unlocks and clears failed attempts using A, then #.
        enter_code(4'ha);
        check_output(8'b1010_0001, "correct password unlocks");

        // Incorrect password increments attempts and clears unlocked.
        enter_code(4'h3);
        check_output(8'b1010_0100, "first incorrect password");

        // Three failed attempts lock the design.
        enter_code(4'h4);
        check_output(8'b1010_1000, "second incorrect password");
        enter_code(4'h5);
        check_output(8'b1010_1110, "third incorrect password locks out");

        // Once locked out, correct password and password changes are ignored.
        enter_code(4'ha);
        check_output(8'b1010_1110, "locked out ignores correct password");
        set_password(4'hd);
        check_output(8'b1010_1110, "locked out ignores password changes");

        $display("PASS");
        $finish;
    end

endmodule

`default_nettype wire
