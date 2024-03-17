import React, { useState, useRef, useEffect } from 'react';
import { createPopper } from '@popperjs/core';

function Tooltip({ tooltipContent, newTooltipContent }) {
  const [visible, setVisible] = useState(false);
  const [content, setContent] = useState(tooltipContent);
  const tooltipRef = useRef(null);
  const popperRef = useRef(null);
  let timeoutId;

  useEffect(() => {
    if (visible) {
      createPopper(tooltipRef.current, popperRef.current, {
        placement: 'bottom',
      });
      // Set a timeout to fade away the tooltip after 3 seconds
      timeoutId = setTimeout(() => {
        setVisible(false);
      }, 3000);
    } else {
      // Clear the timeout if the tooltip is no longer visible
      clearTimeout(timeoutId);
    }
  }, [visible]);

  const handleClick = () => {
    setContent(newTooltipContent);
  };

  return (
    <div
      ref={tooltipRef}
      onMouseEnter={() => setVisible(true)}
      onMouseLeave={() => setVisible(false)}
    >
      {visible && (
        <div
          ref={popperRef}
          className="tooltip-container"
          onClick={handleClick}
        >
          {content}
        </div>
      )}
    </div>
  );
}

export default Tooltip;
