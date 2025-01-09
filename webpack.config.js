const path = require('path');

module.exports = {
  entry: './static/js/site-bundle.js',
  output: {
    filename: 'site-bundle.js',
    path: path.resolve(__dirname, 'static/dist'),
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader', 'postcss-loader'],
      }
    ]
  }
};
