import axios from 'axios'
import settings from '../conf/settings'

const API_BASE_URL = settings.apiBaseUrl;


const apiClient = async ({method, path, data, params, options, headers}) => {
    // remove leading slash from path
    if (path.substring(0, 1) === '/') {
        path = path.substring(1, path.length);
    }

    let defaultHeaders = {
        'Accept': 'application/json'
    };

    if (method === 'post') {
        defaultHeaders['Content-Type'] = 'application/json;charset=UTF-8'
    }

    const config = {
        url: `${API_BASE_URL}/${path}`,
        method: method,
        data: data,
        params: params,
        ...options,
        headers: Object.assign(headers || {}, defaultHeaders)
    };

    return await axios(config);
};

export default apiClient