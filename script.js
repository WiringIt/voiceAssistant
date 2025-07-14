// // Page navigation elements
// const mainPage = document.getElementById('main-page');
// const productPage = document.getElementById('product-page');
// const recordBtn = document.getElementById('record-btn');
// const backBtn = document.getElementById('back-btn');

// // Thumbnail functionality
// const thumbnails = document.querySelectorAll('.thumbnail');
// const mainProductImage = document.querySelector('.product-image img');

// // Size selection functionality
// const sizeButtons = document.querySelectorAll('.size-btn');
// const colorButtons = document.querySelectorAll('.color-btn');

// // Action buttons
// const addToCartBtn = document.querySelector('.add-to-cart-btn');
// const buyNowBtn = document.querySelector('.buy-now-btn');
// const wishlistBtn = document.querySelector('.wishlist-btn');

// // Page transition function
// function showPage(pageToShow, pageToHide) {
//   pageToHide.classList.add('slide-out');
//   pageToHide.classList.remove('active');
  
//   setTimeout(() => {
//     pageToShow.classList.add('active');
//     pageToHide.classList.remove('slide-out');
//   }, 200);
// }

// // Record button click handler
// recordBtn.addEventListener('click', () => {
//   // Add recording animation
//   recordBtn.style.transform = 'scale(0.95)';
//   recordBtn.innerHTML = `
//     <div class="record-icon">
//       <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
//         <circle cx="12" cy="12" r="8" fill="currentColor"/>
//       </svg>
//     </div>
//     <span class="record-text">Listening...</span>
//   `;
  
//   // Simulate voice recognition delay
//   setTimeout(() => {
//     showPage(productPage, mainPage);
    
//     // Reset button after transition
//     setTimeout(() => {
//       recordBtn.style.transform = '';
//       recordBtn.innerHTML = `
//         <div class="record-icon">
//           <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
//             <path d="M12 1C10.34 1 9 2.34 9 4V12C9 13.66 10.34 15 12 15C13.66 15 15 13.66 15 12V4C15 2.34 13.66 1 12 1Z" fill="currentColor"/>
//             <path d="M19 10V12C19 16.42 15.42 20 11 20H13C17.42 20 21 16.42 21 12V10H19Z" fill="currentColor"/>
//             <path d="M7 12V10H5V12C5 16.42 8.58 20 13 20H11C6.58 20 3 16.42 3 12Z" fill="currentColor"/>
//             <path d="M12 22V20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
//             <path d="M8 22H16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
//           </svg>
//         </div>
//         <span class="record-text">Start Recording</span>
//       `;
//     }, 400);
//   }, 1500);
// });

// // Back button click handler
// backBtn.addEventListener('click', () => {
//   showPage(mainPage, productPage);
// });

// // Thumbnail click handlers
// thumbnails.forEach((thumbnail, index) => {
//   thumbnail.addEventListener('click', () => {
//     // Remove active class from all thumbnails
//     thumbnails.forEach(t => t.classList.remove('active'));
    
//     // Add active class to clicked thumbnail
//     thumbnail.classList.add('active');
    
//     // Update main image
//     const newImageSrc = thumbnail.querySelector('img').src.replace('w=200', 'w=800');
//     mainProductImage.src = newImageSrc;
    
//     // Add smooth transition effect
//     mainProductImage.style.opacity = '0';
//     setTimeout(() => {
//       mainProductImage.style.opacity = '1';
//     }, 150);
//   });
// });

// // Size selection handlers
// sizeButtons.forEach(button => {
//   button.addEventListener('click', () => {
//     sizeButtons.forEach(btn => btn.classList.remove('active'));
//     button.classList.add('active');
//   });
// });

// // Color selection handlers
// colorButtons.forEach(button => {
//   button.addEventListener('click', () => {
//     colorButtons.forEach(btn => btn.classList.remove('active'));
//     button.classList.add('active');
//   });
// });

// // Add to cart functionality
// addToCartBtn.addEventListener('click', () => {
//   const originalText = addToCartBtn.textContent;
//   addToCartBtn.textContent = 'Added to Cart!';
//   addToCartBtn.style.background = '#10b981';
  
//   setTimeout(() => {
//     addToCartBtn.textContent = originalText;
//     addToCartBtn.style.background = '#3b82f6';
//   }, 2000);
// });

// // Buy now functionality
// buyNowBtn.addEventListener('click', () => {
//   const originalText = buyNowBtn.textContent;
//   buyNowBtn.textContent = 'Processing...';
//   buyNowBtn.style.background = '#6b7280';
  
//   setTimeout(() => {
//     buyNowBtn.textContent = originalText;
//     buyNowBtn.style.background = '#111827';
//   }, 2000);
// });

// // Wishlist functionality
// wishlistBtn.addEventListener('click', () => {
//   const isWishlisted = wishlistBtn.classList.contains('wishlisted');
  
//   if (isWishlisted) {
//     wishlistBtn.classList.remove('wishlisted');
//     wishlistBtn.style.color = '#6b7280';
//     wishlistBtn.style.borderColor = '#d1d5db';
//   } else {
//     wishlistBtn.classList.add('wishlisted');
//     wishlistBtn.style.color = '#dc2626';
//     wishlistBtn.style.borderColor = '#dc2626';
//   }
// });

// // Add smooth scrolling for mobile
// if (window.innerWidth <= 768) {
//   document.body.style.overflowX = 'hidden';
// }

// // Handle window resize
// window.addEventListener('resize', () => {
//   if (window.innerWidth <= 768) {
//     document.body.style.overflowX = 'hidden';
//   } else {
//     document.body.style.overflowX = 'auto';
//   }
// });
// Page navigation elements
const mainPage = document.getElementById('main-page');
const productPage = document.getElementById('product-page');
const recordBtn = document.getElementById('record-btn');
const backBtn = document.getElementById('back-btn');

// Thumbnail functionality
const thumbnails = document.querySelectorAll('.thumbnail');
const mainProductImage = document.querySelector('.product-image img');

// Size selection functionality
const sizeButtons = document.querySelectorAll('.size-btn');
const colorButtons = document.querySelectorAll('.color-btn');

// Action buttons
const addToCartBtn = document.querySelector('.add-to-cart-btn');
const buyNowBtn = document.querySelector('.buy-now-btn');
const wishlistBtn = document.querySelector('.wishlist-btn');

// Page transition function
function showPage(pageToShow, pageToHide) {
  pageToHide.classList.add('slide-out');
  pageToHide.classList.remove('active');

  setTimeout(() => {
    pageToShow.classList.add('active');
    pageToHide.classList.remove('slide-out');
  }, 200);
}

// Voice synthesis function
function speakText(message) {
  const synth = window.speechSynthesis;
  if (!synth) return;

  const utterance = new SpeechSynthesisUtterance(message);
  utterance.rate = 1;
  utterance.pitch = 1;
  utterance.lang = 'en-US';
  synth.speak(utterance);
}

// Record button click handler
recordBtn.addEventListener('click', () => {
  // Add recording animation
  recordBtn.style.transform = 'scale(0.95)';
  recordBtn.innerHTML = `
    <div class="record-icon">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="8" fill="currentColor"/>
      </svg>
    </div>
    <span class="record-text">Listening...</span>
  `;

  // Simulate voice recognition delay
  setTimeout(() => {
    showPage(productPage, mainPage);

    // Speak suggestion
    speakText("Suggestions for blue denim");

    // Reset button after transition
    setTimeout(() => {
      recordBtn.style.transform = '';
      recordBtn.innerHTML = `
        <div class="record-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 1C10.34 1 9 2.34 9 4V12C9 13.66 10.34 15 12 15C13.66 15 15 13.66 15 12V4C15 2.34 13.66 1 12 1Z" fill="currentColor"/>
            <path d="M19 10V12C19 16.42 15.42 20 11 20H13C17.42 20 21 16.42 21 12V10H19Z" fill="currentColor"/>
            <path d="M7 12V10H5V12C5 16.42 8.58 20 13 20H11C6.58 20 3 16.42 3 12Z" fill="currentColor"/>
            <path d="M12 22V20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <path d="M8 22H16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </div>
        <span class="record-text">Start Recording</span>
      `;
    }, 400);
  }, 1500);
});

// Back button click handler
backBtn.addEventListener('click', () => {
  showPage(mainPage, productPage);
});

// Thumbnail click handlers
thumbnails.forEach((thumbnail, index) => {
  thumbnail.addEventListener('click', () => {
    thumbnails.forEach(t => t.classList.remove('active'));
    thumbnail.classList.add('active');

    const newImageSrc = thumbnail.querySelector('img').src.replace('w=200', 'w=800');
    mainProductImage.src = newImageSrc;

    mainProductImage.style.opacity = '0';
    setTimeout(() => {
      mainProductImage.style.opacity = '1';
    }, 150);
  });
});

// Size selection handlers
sizeButtons.forEach(button => {
  button.addEventListener('click', () => {
    sizeButtons.forEach(btn => btn.classList.remove('active'));
    button.classList.add('active');
  });
});

// Color selection handlers
colorButtons.forEach(button => {
  button.addEventListener('click', () => {
    colorButtons.forEach(btn => btn.classList.remove('active'));
    button.classList.add('active');
  });
});

// Add to cart functionality
addToCartBtn.addEventListener('click', () => {
  const originalText = addToCartBtn.textContent;
  addToCartBtn.textContent = 'Added to Cart!';
  addToCartBtn.style.background = '#10b981';

  setTimeout(() => {
    addToCartBtn.textContent = originalText;
    addToCartBtn.style.background = '#3b82f6';
  }, 2000);
});

// Buy now functionality
buyNowBtn.addEventListener('click', () => {
  const originalText = buyNowBtn.textContent;
  buyNowBtn.textContent = 'Processing...';
  buyNowBtn.style.background = '#6b7280';

  setTimeout(() => {
    buyNowBtn.textContent = originalText;
    buyNowBtn.style.background = '#111827';
  }, 2000);
});

// Wishlist functionality
wishlistBtn.addEventListener('click', () => {
  const isWishlisted = wishlistBtn.classList.contains('wishlisted');

  if (isWishlisted) {
    wishlistBtn.classList.remove('wishlisted');
    wishlistBtn.style.color = '#6b7280';
    wishlistBtn.style.borderColor = '#d1d5db';
  } else {
    wishlistBtn.classList.add('wishlisted');
    wishlistBtn.style.color = '#dc2626';
    wishlistBtn.style.borderColor = '#dc2626';
  }
});

// Add smooth scrolling for mobile
if (window.innerWidth <= 768) {
  document.body.style.overflowX = 'hidden';
}

// Handle window resize
window.addEventListener('resize', () => {
  if (window.innerWidth <= 768) {
    document.body.style.overflowX = 'hidden';
  } else {
    document.body.style.overflowX = 'auto';
  }
});
