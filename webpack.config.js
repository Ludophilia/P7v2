module.exports = {
    mode: "production",
    entry: "./app/static/src/js/entry.js",
    module: {
        rules : [
            {
                test:/.s[ca]ss$/i,
                use: ["style-loader", "css-loader", "sass-loader"]
            }
        ]
    },
    output: {
        path: `${__dirname}/app/static/dist`,
        filename: "bundle.js"
    }
}