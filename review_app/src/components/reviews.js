import React, { useState, useEffect, useRef } from 'react';

import Stars from './stars';

import styles from './reviews.module.css';

function Reviews(props) {
    const { 
        reviews,
        onReviewSelected, 
        onShowFavoritesChange,
        onBeforeChange,
        onFavorite,
        onLoadMore
    } = props;


    const onScroll = (e) => {
        // When we're around 80%, ask for the next set of data.
        if( e.target.scrollTop / (e.target.scrollHeight - e.target.offsetHeight) >= 0.8) {
            onLoadMore();
        }
    };
    
    const onFavoriteChange = (e, review) => { 
        e.preventDefault(); 
        e.stopPropagation(); 

        review.isFavorite = !review.isFavorite;
        onFavorite(review); 
    }

    return (
        <div className={styles.reviews}>
            <header>
                <div className="corset">
                    <h1>Reviews</h1>
                    <div className={styles.options}>
                        <span className={styles.showFavorites}>
                            <input id="cbxShowFavorites" type='checkbox' 
                                onChange={onShowFavoritesChange}
                            />
                            <label htmlFor="cbxShowFavorites">Show Favorites Only</label>
                        </span>
                        <span className={styles.before}>
                            <label htmlFor="dtlBefore">Before</label>
                            <input id="dtlBefore" type="datetime-local" 
                                onChange={onBeforeChange}
                            />
                        </span>
                    </div>
                </div>
            </header>
            <div className={styles.scrollArea}
                onScroll={onScroll}
            >
                <div className="corset">
                    <ul>
                        { reviews.map(r => (
                            <li key={r.id}
                                className={styles.review}
                                onClick={() => onReviewSelected(r.id)}
                            >
                                <span 
                                    className={styles.favorite + (r.isFavorite ? ` ${styles.isFavorite}` : "")}
                                    onClick={(e) => onFavoriteChange(e,r)}
                                >&#10084;</span>
                                <span className={styles.id}>{r.id}</span>
                                <span className={styles.stars}><Stars value={r.stars} /></span>
                                <span className={styles.text}>{r.text}</span>
                                <span className={styles.date}>{new Date(r.date).toLocaleString()}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
}

export default Reviews;