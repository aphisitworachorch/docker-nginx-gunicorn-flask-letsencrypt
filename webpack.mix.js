let mix = require('webpack-mix');

mix.sass('style/sass/app.sass', 'src/static/css').js('style/js/app.js', 'src/static/js').options({
    processCssUrls: true,
    purifyCss: false,
    uglify: {
        uglifyOptions: {
            compress: {
                drop_console: true,
                drop_debugger: true
            }
        }
    }
});
