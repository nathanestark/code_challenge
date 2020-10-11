import React, { useState, useEffect } from 'react';

import { getReview, updateReview } from '../api';

import Stars from './stars';

import styles from './review.module.css';

function Review(props) {
    const { id, onClose, onFavorite } = props;
    const [ review, setReview ] = useState(null);

    useEffect(() => {
        (async () => {

            const review = await getReview(id);
            setReview(review);
        })();
    }, [id]);

    const onFavoriteChange = async () => {
        // Update local copy.
        review.isFavorite = !review.isFavorite;
        setReview(review);
        const newReview = await onFavorite(review);
        // Do it again in case it was rolled back.
        setReview(newReview);
    }

    return (
        <div className={styles.review}>
            <div className={styles.content}>
                <header>
                    <span 
                        className={styles.favorite + (review && review.isFavorite ? ` ${styles.isFavorite}` : "")}
                        onClick={onFavoriteChange}
                    >&#10084;</span>
                    <h1>{review ? review.id : ""}</h1>
                    <button onClick={onClose}>Close</button>
                </header>
                <div className={styles.body}>
                    {review ? (
                        <>
                            <span>
                                <label>UserId</label>
                                <span>{review.userId}</span>
                            </span>
                            <span>
                                <label>BusinessId</label>
                                <span>{review.businessId}</span>
                            </span>
                            <span>
                                <label>Stars</label>
                                <span><Stars value={review.stars}/></span>
                            </span>
                            <span>
                                <label>Useful</label>
                                <span>{review.useful}</span>
                            </span>
                            <span>
                                <label>Funny</label>
                                <span>{review.funny}</span>
                            </span>
                            <span>
                                <label>Cool</label>
                                <span>{review.cool}</span>
                            </span>
                            <span>
                                <label>Date</label>
                                <span>{new Date(review.date).toLocaleString()}</span>
                            </span>
                            <label>Content</label>
                            <p>{review.text}</p>
                        </>
                    ) : null}
                </div>
            </div>
        </div>
    )
}

export default Review;