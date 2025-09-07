function runge
    clf; 
    hold on; 
    grid on; 
    box on;
    axis([-5 5 -10 10]);
    title('Runge phenomenon for x in [-5,5]'); 

    f = @(x) 1./(1+x);

    % --- 函數曲線（避開 x=-1） ---
    x = linspace(-5,5,4000);
    x = x(abs(x+1) > 1e-6);   % 去掉接近 -1 的點
    y = f(x);
    plot(x, y, 'r', 'LineWidth', 2);
    text(0.05,0.9,'f(x)=1/(1+x)','Units','normalized','Color','r');

    for n = [6 10 14]           % 設定節點數
        x_nodes = linspace(-5,5,n);
        x_nodes = x_nodes(abs(x_nodes+1) > 1e-8); % 刪掉 -1
        y_nodes = f(x_nodes);

        p = polyfit(x_nodes, y_nodes, numel(x_nodes)-1);
        f_interp = polyval(p, x);

        n_nodes = numel(x_nodes);
        label_str = sprintf('%d nodes', n_nodes);
        h = plot(x, f_interp);
        set(h, 'LineWidth', 1.2);
        set(h, 'DisplayName', label_str);
    end

    legend('f(x)','6 nodes','10 nodes','14 nodes','Location','best');
    hold off;
end
