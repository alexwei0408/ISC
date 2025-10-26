function runge
    clf; 
    hold on; 
    grid on; 
    box on;

    axis([-5 5 -0.1 1.1]);                         
    title('Polynomial interpolation with uniform nodes on [-5,5]'); 

    f = @(x) 1./(1 + (x.^2));
    x = linspace(-5, 5, 4000);
    y = f(x);
    plot(x, y, 'r', 'LineWidth', 2, 'DisplayName', 'f(x)=1/(1+x^2)');
    text(0.05, 0.9, 'f(x)=1/(1+x^2)', 'Units','normalized', 'Color','r');


    for n = [6 10 14]                
        x_nodes = linspace(-5, 5, n);
        y_nodes = f(x_nodes);

        p = polyfit(x_nodes, y_nodes, n-1);   
        y_interp = polyval(p, x);

        label_str = sprintf('%d nodes (deg %d)', n, n-1);
        h = plot(x, y_interp, 'LineWidth', 1.2, 'DisplayName', label_str);

        plot(x_nodes, y_nodes, 'o', 'MarkerSize', 4, 'HandleVisibility','off', ...
             'Color', h.Color);
    end

    legend('Location','best');
    hold off;
end