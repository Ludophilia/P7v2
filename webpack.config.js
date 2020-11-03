module.exports = {
    mode: "production",
    entry: "./app/static/src/js/entry.js",
    module: {
        rules : [
            {
                test:/.s[ca]ss$/i,
                use: ["style-loader", "css-loader", "sass-loader"]
            },
            {
                test:/.(woff|woff2|eot|ttf|otf)$/i,
                use: ["file-loader"]
            },
        ]
    },
    output: {
        path: `${__dirname}/app/static/dist`,
        filename: "bundle.js"
    }
}