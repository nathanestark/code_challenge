import React from 'react';

import styles from './stars.module.css'

function Stars(props) {
    const { value } = props;

    return (
        <span className={styles.stars}>
            <span className={ value >= 1 ? styles.on : ""}>&#9733;</span>
            <span className={ value >= 2 ? styles.on : ""}>&#9733;</span>
            <span className={ value >= 3 ? styles.on : ""}>&#9733;</span>
            <span className={ value >= 4 ? styles.on : ""}>&#9733;</span>
            <span className={ value >= 5 ? styles.on : ""}>&#9733;</span>
        </span>
    )
}

export default Stars;