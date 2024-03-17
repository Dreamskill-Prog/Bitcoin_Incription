import React, { useState, useRef, useEffect } from 'react';
import { createPopper } from '@popperjs/core';
import { FaCopy } from 'react-icons/fa';
import 'react-popper-tooltip/dist/styles.css';

function CopyToClipboard({ text }) {
  const [isHovered, setIsHovered] = useState(false);
  const [visible, setVisible] = useState(false);
  const [content, setContent] = useState("Click to Copy Deposit Address");
  const tooltipRef = useRef(null);
  const popperRef = useRef(null);
  let timeoutId;

  useEffect(() => {
    if (visible) {
      createPopper(tooltipRef.current, popperRef.current, {
        placement: 'bottom-end',
      });
      // Set a timeout to fade away the tooltip after 3 seconds
      timeoutId = setTimeout(() => {
        setVisible(false);
      }, 6000);
    } else {
      // Clear the timeout if the tooltip is no longer visible
      clearTimeout(timeoutId);
    }
  }, [visible]);

  const handleCopyClick = () => {
    navigator.clipboard.writeText(text);
    setContent("Copied!");
  };


  const handleMouseEnter = () => {
    setIsHovered(true);
    setVisible(true)
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
    setVisible(false)
    setContent("Click to Copy Deposit Address");
  };

  return (
    <span
      ref={tooltipRef}
      style={{ backgroundColor: isHovered ? 'blue' : 'transparent', cursor: 'pointer' }}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onClick={handleCopyClick}
    >
      {text}{' '}
      <FaCopy style={{ verticalAlign: 'middle' }} />

      {visible && (
        <div ref={popperRef} className="tooltip-container">
          {content}
        </div>
      )}
    </span>
  );
};

export default CopyToClipboard;
