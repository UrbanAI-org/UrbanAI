import React, { useState, useEffect, useRef } from 'react';

const Loading =({word}) => {
    return (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(0, 0, 0, 0.5)', // semi-transparent gray background
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            zIndex: 9999, // make sure it appears above other elements
          }}
        >
          <p style={{ color: '#fff', fontSize: '24px' }}>{word}</p> {/* "Loading" text */}
        </div>
    );
};
export default Loading;
