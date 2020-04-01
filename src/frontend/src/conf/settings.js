const settings = {
    apiBaseUrl: process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8080/api/v1",
    siteUrl: process.env.REACT_APP_SITE_URL || "http://127.0.0.1:3000/",
    gameTtl: 3 * 60
};

export default settings