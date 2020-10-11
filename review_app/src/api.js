const API_ROOT = process.env.REACT_APP_API_ROOT;

export async function listReviews(opts) {
    // Provide healthy defaults.
    opts = Object.assign({ 
        limit: 100, 
        continuationToken: null, 
        before: null, 
        favoritesOnly: false 
    }, opts);

    let path = `${API_ROOT}/reviews`;
    const queryString = [];
    if(opts.continuationToken) 
        queryString.push(`continuationToken=${encodeURIComponent(opts.continuationToken)}`);
    else if(opts.before) 
        queryString.push(`before=${encodeURIComponent(new Date(opts.before).toISOString())}`);

    if(opts.favoritesOnly)
        queryString.push(`favorites`);
    
    // Ensure limit is correct
    if(typeof opts.limit !== 'number' || opts.limit < 1 || opts.limit > 1000)
        throw new Error("Option 'limit' must be an integer number between 1 and 1000");
    else
        opts.limit = Math.floor(opts.limit);
    queryString.push(`limit=${opts.limit}`);

    if(queryString.length > 0)
        path += `?${queryString.join('&')}`;

        const response = await fetch(path, {
        method: 'GET'
    });

    if(!response.ok) {
        throw new Error(`Error in listReviews: ${response.statusCode} (${response.statusMessage})`)
    }
    return await response.json();
}

export async function getReview(reviewId) {
    if(!reviewId || typeof reviewId !== 'string') throw new Error("Must provide a valid reviewId");
    
    const response = await fetch(`${API_ROOT}/reviews/${reviewId}`, {
        method: 'GET'
    });

    if(!response.ok) {
        // Just return null if we couldn't find what we were looking for.
        if(response.statusCode == 404)
            return null; 

        throw new Error(`Error in getReview: ${response.statusCode} (${response.statusMessage})`)
    }
    return await response.json();
}

export async function updateReview(reviewId, isFavorite) {
    if(!reviewId || typeof reviewId !== 'string') throw new Error("Must provide a valid reviewId");

    // For now, 'isFavorite' is the only property we can modify.
    const body = {
        isFavorite: !!isFavorite
    }

    const response = await fetch(`${API_ROOT}/reviews/${reviewId}`, {
        method: 'PUT',
        headers: {
            "content-type": "application/json"
        },
        body: JSON.stringify(body)
    });

    if(!response.ok) {
        // Just return null if we couldn't find what we were looking for.
        if(response.statusCode == 404)
            return null; 

        throw new Error(`Error in updateReview: ${response.statusCode} (${response.statusMessage})`)
    }
    return await response.json();
}