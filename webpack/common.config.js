const path = require("path");
const BundleTracker = require("webpack-bundle-tracker");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const WebpackBar = require("webpackbar");
const CopyWebpackPlugin = require("copy-webpack-plugin");
const { ProvidePlugin } = require("webpack");
const Dotenv = require("dotenv-webpack");

module.exports = {
  target: "web",
  context: path.join(__dirname, "../"),
  entry: {
    project: path.resolve(__dirname, "../static/js/project"),
    vendors: path.resolve(__dirname, "../static/js/vendors"),
    tenants: path.resolve(__dirname, "../static/js/tenants/index"),
  },
  output: {
    path: path.resolve(__dirname, "../assets/webpack_bundles/"),
    publicPath: "/static/webpack_bundles/",
    filename: "js/[name]-[fullhash].js",
    chunkFilename: "js/[name]-[fullhash].js",
    clean: true,
  },
  plugins: [
    new BundleTracker({
      path: path.resolve(path.join(__dirname, "../assets")),
      filename: "webpack-stats.json",
    }),
    new WebpackBar({ name: "compiler" }),
    new MiniCssExtractPlugin({ filename: "css/[name].[contenthash].css" }),
    new CopyWebpackPlugin({
      patterns: [
        {
          from: path.resolve(__dirname, "../static/images/favicons"),
          to: "images/favicons",
        },
        {
          from: path.resolve(__dirname, "../static/images/logos"),
          to: "images/logos",
        },
        {
          from: path.resolve(__dirname, "../static/images/apps"),
          to: "images/apps",
        },
        {
          from: path.resolve(__dirname, "../static/images/icons"),
          to: "images/icons",
        },
        {
          from: path.resolve(__dirname, "../static/images/banner"),
          to: "images/banner",
        },
        {
          from: path.resolve(__dirname, "../static/images/events"),
          to: "images/events",
        },
        {
          from: path.resolve(__dirname, "../static/images/profiles"),
          to: "images/profiles",
        },
      ],
    }),
    new Dotenv({ path: path.resolve(__dirname, "../.env") }),
    new ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      axios: "axios",
      "window.jQuery": "jquery",
      "window.$": "jquery",
    }),
  ],
  module: {
    rules: [
      {
        test: /\.[jt]sx?$/,
        loader: "babel-loader",
        exclude: /node_modules/,
      },
      {
        test: /\.(png|jpe?g|gif|svg)$/i,
        type: "asset/resource",
        generator: {
          filename: "images/[name]-[contenthash][ext][query]",
        },
      },
      {
        test: /\.(woff2?|eot|ttf|otf)$/i,
        type: "asset/resource",
        generator: {
          filename: "fonts/[name]-[contenthash][ext][query]",
        },
      },
      {
        test: /\.s?css$/i,
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader",
          {
            loader: "postcss-loader",
            options: {
              postcssOptions: {
                plugins: ["postcss-preset-env", "autoprefixer", "pixrem"],
              },
            },
          },
          "sass-loader",
        ],
      },
    ],
  },
  resolve: {
    modules: ["node_modules", path.resolve(__dirname, "../static/src")],
    extensions: [".js", ".jsx", ".ts", ".tsx"],
    alias: {
      "@": path.resolve(__dirname, "../static/src"),
      "@images": path.resolve(__dirname, "../static/images"),
    },
  },
  devServer: {
    proxy: {
      "/api": {
        target: process.env.BACKEND_URL,
        changeOrigin: true,
      },
    },
  },
};
