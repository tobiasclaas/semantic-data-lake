const path = require('path')

module.exports = {
  entry: { main: './src/main.tsx' },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'babel-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.(png|svg|jpg|gif)$/,
        loader: 'file-loader',
        options: {
          name: 'resources/img/[name].[ext]',
        },
      },
      {
        test: /\.(ttf|woff|eot)$/,
        loader: 'file-loader',
        options: {
          name: 'resources/fonts/[name].[ext]',
        },
      },
      {
        test: /\.(html)$/,
        loader: 'file-loader',
        options: {
          name: '[name].[ext]',
        },
      },
    ],
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
  },
  output: {
    filename: '[name].js',
    path: path.join(__dirname, 'public', 'dist'),
    chunkFilename: '[id].[chunkhash].js'
  },
  optimization: {
    usedExports: true,
  }
}
