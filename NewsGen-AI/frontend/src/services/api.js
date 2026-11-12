
import axios from "axios";

const API = axios.create({
    baseURL: "http://127.0.0.1:8000",
    timeout: 30000
});

// Get dashboard statistics
export const getDashboardStats = async () => {
    const response = await API.get("/api/dashboard/stats");
    return response.data;
};

// Get paginated articles
export const getArticles = async (page = 1, limit = 10) => {
    const response = await API.get("/api/articles", {
        params: { page, limit }
    });
    return response.data;
};

// Get latest articles
export const getLatestArticles = async (limit = 5) => {
    const response = await API.get("/api/articles/latest", {
        params: { limit }
    });
    return response.data;
};

// Get categories
export const getCategories = async () => {
    const response = await API.get("/api/categories");
    return response.data;
};

// Search articles
export const searchArticles = async (keyword) => {
    const response = await API.get("/api/articles/search", {
        params: { keyword }
    });
    return response.data;
};

// Filter articles by category
export const getArticlesByCategory = async (category) => {
    const response = await API.get(
        `/api/articles/category/${encodeURIComponent(category)}`
    );
    return response.data;
};

export default API;
