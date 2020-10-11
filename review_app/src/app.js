import React, { useState, useEffect } from 'react';

import { listReviews, getReview, updateReview } from './api'

import Reviews from './components/reviews';
import Review from './components/review';

import './app.css';

function App() {
    const [reviews, setReviews] = useState([]);
    const [curReview, setCurReview] = useState(null);

    const [continuationToken, setContinuationToken] = useState(null);
    const [beforeDate, setBeforeDate] = useState();
    const [favoritesOnly, setFavoritesOnly] = useState(false); 

    useEffect(() => {
        (async () => {
            const opts = {};
            if(beforeDate) opts.before = beforeDate;
            if(continuationToken) opts.continuationToken = continuationToken;
            if(favoritesOnly) opts.favoritesOnly = favoritesOnly;
            console.log("Listing more from", opts.continuationToken);
            const reviews = await listReviews(opts);
            setReviews((prev) => prev.concat(reviews));
        })();
    }, [continuationToken, beforeDate, favoritesOnly]);

    const onLoadMore = () => {
        console.log("NUM REVIEWS", reviews.length);
        setContinuationToken(reviews[reviews.length-1].continuationToken);
    }

    const onShowFavoritesChange = () => {
        // Reset reviews
        setReviews([]);
        setContinuationToken(null);
        setFavoritesOnly(prev => !prev);    
    }

    // We don't *really* want to fetch a new list each time we change this value.
    // This can be unnecessarily spammy on the backend.
    // Instead, we should delay a bit and once we're sure they're done changing
    // the date, then update the view.
    const onBeforeChange = (e) => {
        const newDate = e.target.value;

        // Reset reviews
        setReviews([]);
        setContinuationToken(null);
        setBeforeDate(newDate);
    }

    const onFavorite = async (review) => {
        // Update the review now so our UI reflects the change immediately.
        setReviews(prev => prev.map(r => r.id == review.id ? review : r));

        // Update it remotely.
        const newReview = await updateReview(review.id, review.isFavorite);

        // Use the new object returned from the remote call.
        setReviews(prev => prev.map(r => r.id == newReview.id ? newReview : r));

        return newReview;
    }

    return (
        <div className="app">
            <Reviews
                reviews={reviews}
                onReviewSelected={setCurReview}
                onShowFavoritesChange={onShowFavoritesChange}
                onBeforeChange={onBeforeChange}
                onFavorite={onFavorite}
                onLoadMore={onLoadMore}
            />
            {curReview ? (
                <Review
                    id={curReview}
                    onClose={() => setCurReview(null)}
                    onFavorite={onFavorite}
                />
            ) : null}
        </div>
    );
}

export default App;
