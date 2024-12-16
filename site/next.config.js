/** @type {import('next').NextConfig} */
const path = require("path");

const nextConfig = {
    webpack: (config, { isServer }) => {
        if (!isServer) {
            config.resolve.alias["yjs"] = path.resolve(__dirname, "node_modules/yjs");
        }
        return config;
    },
};

module.exports = nextConfig;
