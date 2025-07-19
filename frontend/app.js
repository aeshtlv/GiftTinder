// Initialize Telegram WebApp
let tg = window.Telegram.WebApp;
tg.expand();
tg.ready();

// App state
let currentUser = null;
let currentGift = null;
let gifts = [];
let matches = [];

// API base URL
const API_BASE = 'http://localhost:8000/api';

// DOM elements
const loadingScreen = document.getElementById('loading');
const swipeScreen = document.getElementById('swipe-screen');
const profileScreen = document.getElementById('profile-screen');
const matchesScreen = document.getElementById('matches-screen');
const matchNotification = document.getElementById('match-notification');

// Initialize app
async function initApp() {
    try {
        // Get user data from Telegram
        currentUser = tg.initDataUnsafe?.user;
        if (!currentUser) {
            throw new Error('User data not available');
        }

        // Register user with backend
        await registerUser();

        // Load initial data
        await Promise.all([
            loadNextGift(),
            loadUserProfile(),
            loadMatches()
        ]);

        // Show main screen
        showScreen('swipe-screen');
        
    } catch (error) {
        console.error('App initialization failed:', error);
        showError('Ошибка инициализации приложения');
    }
}

// Register user with backend
async function registerUser() {
    try {
        const response = await fetch(`${API_BASE}/user`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Telegram-Init-Data': tg.initData
            }
        });

        if (!response.ok) {
            throw new Error('Failed to register user');
        }

        const userData = await response.json();
        console.log('User registered:', userData);
        
    } catch (error) {
        console.error('User registration failed:', error);
        throw error;
    }
}

// Load next gift to swipe
async function loadNextGift() {
    try {
        const response = await fetch(`${API_BASE}/next_gift/${currentUser.id}`);
        
        if (!response.ok) {
            throw new Error('Failed to load next gift');
        }

        const giftData = await response.json();
        
        if (giftData.message === 'No more gifts to swipe') {
            showNoMoreGifts();
            return;
        }

        currentGift = giftData;
        displayGift(currentGift);
        
    } catch (error) {
        console.error('Failed to load next gift:', error);
        showError('Ошибка загрузки подарка');
    }
}

// Display gift on screen
function displayGift(gift) {
    const giftImg = document.getElementById('gift-img');
    const giftName = document.getElementById('gift-name');
    const giftDescription = document.getElementById('gift-description');

    giftImg.src = gift.image_url || 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjRjBGMEYwIi8+Cjx0ZXh0IHg9IjEwMCIgeT0iMTAwIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTYiIGZpbGw9IiM5OTk5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj7Qn9C+0LvRg9GH0LjRgtGMINGP0LfQvdC10YHRgtC90L7QuSDQv9C+0LvQsNGC0YvQuyDQv9GA0L7QsdC10LvRj9C30LDRgtC10LvRjzwvdGV4dD4KPC9zdmc+';
    giftName.textContent = gift.name || 'Неизвестный подарок';
    giftDescription.textContent = gift.description || 'Описание недоступно';

    // Show gift card
    document.getElementById('gift-card').style.display = 'block';
    document.getElementById('no-more-gifts').style.display = 'none';
}

// Show no more gifts message
function showNoMoreGifts() {
    document.getElementById('gift-card').style.display = 'none';
    document.getElementById('no-more-gifts').style.display = 'block';
}

// Handle swipe action
async function handleSwipe(isLike) {
    if (!currentGift) return;

    try {
        // Add swiping animation
        const giftCard = document.getElementById('gift-card');
        giftCard.classList.add('swiping');

        // Send swipe to backend
        const response = await fetch(`${API_BASE}/swipe`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                telegram_id: currentUser.id,
                gift_id: currentGift.id,
                is_like: isLike
            })
        });

        if (!response.ok) {
            throw new Error('Failed to record swipe');
        }

        const result = await response.json();
        
        // Check for match
        if (isLike && result.is_match) {
            showMatchNotification();
        }

        // Load next gift
        setTimeout(() => {
            giftCard.classList.remove('swiping');
            loadNextGift();
        }, 300);

    } catch (error) {
        console.error('Swipe failed:', error);
        showError('Ошибка при свайпе');
    }
}

// Load user profile
async function loadUserProfile() {
    try {
        const [userResponse, giftsResponse, matchesResponse] = await Promise.all([
            fetch(`${API_BASE}/user/${currentUser.id}`),
            fetch(`${API_BASE}/gifts/${currentUser.id}`),
            fetch(`${API_BASE}/matches/${currentUser.id}`)
        ]);

        if (userResponse.ok) {
            const userData = await userResponse.json();
            displayUserProfile(userData);
        }

        if (giftsResponse.ok) {
            const giftsData = await giftsResponse.json();
            displayUserGifts(giftsData);
        }

        if (matchesResponse.ok) {
            const matchesData = await matchesResponse.json();
            updateStats(matchesData.length);
        }

    } catch (error) {
        console.error('Failed to load profile:', error);
    }
}

// Display user profile
function displayUserProfile(userData) {
    const userName = document.getElementById('user-name');
    const userUsername = document.getElementById('user-username');
    const userAvatar = document.getElementById('user-avatar');

    userName.textContent = userData.first_name || 'Пользователь';
    userUsername.textContent = userData.username ? `@${userData.username}` : 'Без username';
    
    // Set default avatar if no photo
    userAvatar.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODAiIGhlaWdodD0iODAiIHZpZXdCb3g9IjAgMCA4MCA4MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iNDAiIGN5PSI0MCIgcj0iNDAiIGZpbGw9IiM2NjdFRUEiLz4KPHN2ZyB4PSIyMCIgeT0iMjAiIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJ3aGl0ZSI+CjxwYXRoIGQ9Ik0xMiAxMmMyLjIxIDAgNC0xLjc5IDQtNHMtMS43OS00LTQtNC00IDEuNzktNCA0IDEuNzkgNCA0IDR6bTAgMmMtMi42NyAwLTggMS4zNC04IDR2MmgxNnYtMmMwLTIuNjYtNS4zMy00LTgtNHoiLz4KPC9zdmc+Cjwvc3ZnPgo=';
}

// Display user gifts
function displayUserGifts(giftsData) {
    const giftsList = document.getElementById('my-gifts-list');
    const giftsCount = document.getElementById('gifts-count');
    
    giftsCount.textContent = giftsData.length;
    giftsList.innerHTML = '';

    giftsData.forEach(gift => {
        const giftItem = document.createElement('div');
        giftItem.className = 'gift-item';
        giftItem.innerHTML = `
            <img src="${gift.image_url || 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjYwIiBoZWlnaHQ9IjYwIiBmaWxsPSIjRjBGMEYwIi8+Cjx0ZXh0IHg9IjMwIiB5PSIzMCIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEyIiBmaWxsPSIjOTk5OTk5IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+0J/QvtC70YPRh9C40YLRjCDRj9C30L3QtdGB0YLRvdC+0Lkg0L/QvtC70LDRgtGL0Lsg0L/RgNC+0LHQtdC70Y/Qt9Cw0YLQtdC70Y88L3RleHQ+Cjwvc3ZnPgo='}" alt="${gift.name}">
            <p>${gift.name}</p>
        `;
        giftsList.appendChild(giftItem);
    });
}

// Load matches
async function loadMatches() {
    try {
        const response = await fetch(`${API_BASE}/matches/${currentUser.id}`);
        
        if (response.ok) {
            matches = await response.json();
            displayMatches(matches);
        }
        
    } catch (error) {
        console.error('Failed to load matches:', error);
    }
}

// Display matches
function displayMatches(matchesData) {
    const matchesList = document.getElementById('matches-list');
    const noMatches = document.getElementById('no-matches');
    const matchesCount = document.getElementById('matches-count');
    
    matchesCount.textContent = matchesData.length;
    
    if (matchesData.length === 0) {
        matchesList.style.display = 'none';
        noMatches.style.display = 'block';
        return;
    }

    matchesList.style.display = 'block';
    noMatches.style.display = 'none';
    matchesList.innerHTML = '';

    matchesData.forEach(match => {
        const matchItem = document.createElement('div');
        matchItem.className = 'match-item';
        matchItem.innerHTML = `
            <div class="match-avatar">
                ${match.other_user.first_name ? match.other_user.first_name.charAt(0).toUpperCase() : '?'}
            </div>
            <div class="match-info">
                <h4>${match.other_user.first_name || 'Пользователь'}</h4>
                <p>@${match.other_user.username || 'username'}</p>
            </div>
        `;
        matchesList.appendChild(matchItem);
    });
}

// Update stats
function updateStats(matchesCount) {
    document.getElementById('matches-count').textContent = matchesCount;
}

// Show match notification
function showMatchNotification() {
    const notification = document.getElementById('match-notification');
    const matchUserName = document.getElementById('match-user-name');
    
    matchUserName.textContent = 'Вы понравились друг другу!';
    notification.style.display = 'flex';
    
    // Auto hide after 3 seconds
    setTimeout(() => {
        notification.style.display = 'none';
    }, 3000);
}

// Show screen
function showScreen(screenId) {
    // Hide all screens
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    
    // Show target screen
    document.getElementById(screenId).classList.add('active');
}

// Show error message
function showError(message) {
    tg.showAlert(message);
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Swipe buttons
    document.getElementById('like-btn').addEventListener('click', () => handleSwipe(true));
    document.getElementById('dislike-btn').addEventListener('click', () => handleSwipe(false));
    
    // Navigation buttons
    document.getElementById('profile-btn').addEventListener('click', () => {
        showScreen('profile-screen');
        loadUserProfile();
    });
    
    document.getElementById('matches-btn').addEventListener('click', () => {
        showScreen('matches-screen');
        loadMatches();
    });
    
    // Back buttons
    document.getElementById('back-btn').addEventListener('click', () => showScreen('swipe-screen'));
    document.getElementById('back-btn-matches').addEventListener('click', () => showScreen('swipe-screen'));
    
    // Refresh button
    document.getElementById('refresh-btn').addEventListener('click', () => {
        showScreen('swipe-screen');
        loadNextGift();
    });
    
    // Match notification
    document.getElementById('view-match-btn').addEventListener('click', () => {
        document.getElementById('match-notification').style.display = 'none';
        showScreen('matches-screen');
        loadMatches();
    });
    
    // Initialize app
    initApp();
});

// Handle swipe gestures
let startX = 0;
let startY = 0;
let currentX = 0;
let currentY = 0;

document.addEventListener('touchstart', (e) => {
    startX = e.touches[0].clientX;
    startY = e.touches[0].clientY;
});

document.addEventListener('touchmove', (e) => {
    currentX = e.touches[0].clientX;
    currentY = e.touches[0].clientY;
});

document.addEventListener('touchend', () => {
    const deltaX = currentX - startX;
    const deltaY = currentY - startY;
    
    // Only handle horizontal swipes
    if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50) {
        if (deltaX > 0) {
            // Swipe right - like
            handleSwipe(true);
        } else {
            // Swipe left - dislike
            handleSwipe(false);
        }
    }
}); 