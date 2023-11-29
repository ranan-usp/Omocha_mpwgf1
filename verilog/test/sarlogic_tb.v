`timescale 1ns/1ps

module sarlogic_tb;

    reg clk, rstn, en, comp, cal;
    wire valid, sample, clkc;
    wire [9:0] result, ctlp, ctln;
    wire [4:0] trim, trimb;

    // インスタンス化
    sarlogic uut (
        .clk(clk),
        .rstn(rstn),
        .en(en),
        .comp(comp),
        .cal(cal),
        .valid(valid),
        .result(result),
        .sample(sample),
        .ctlp(ctlp),
        .ctln(ctln),
        .trim(trim),
        .trimb(trimb),
        .clkc(clkc)
    );

    // クロック生成
    always #5 clk = ~clk;

    // テストシナリオ
    initial begin
        // 初期化
        clk = 0;
        rstn = 0;
        en = 0;
        comp = 0;
        cal = 0;

        // リセット解除
        #10 rstn = 1;

        // 校正信号を試す
        #20 cal = 1;
        #10 cal = 0;

        // 有効化信号を試す
        #30 en = 1;

        // コンパレータの出力を変化させる
        // ここでは、シンプルな例としてランダムな値を生成
        // 実際のシナリオでは、特定のパターンを適用することが一般的
        repeat (20) begin
            #10 comp = $random;
        end

        // テスト終了
        #100 $finish;
    end

endmodule
