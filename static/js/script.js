console.log("🔥 JS Loaded");


// State management
        let isMenuOpen = false;
        let isScrolled = false;

        // Navigation functionality
        function scrollToSection(href) {
            const element = document.querySelector(href);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth' });
            }
            closeMobileMenu();
        }

        function toggleMobileMenu() {
            isMenuOpen = !isMenuOpen;
            const mobileNav = document.getElementById('mobileNav');
            const menuIcon = document.querySelector('.menu-icon');
            const closeIcon = document.querySelector('.close-icon');

            if (isMenuOpen) {
                mobileNav.classList.add('open');
                menuIcon.style.display = 'none';
                closeIcon.style.display = 'block';
            } else {
                mobileNav.classList.remove('open');
                menuIcon.style.display = 'block';
                closeIcon.style.display = 'none';
            }
        }

        function closeMobileMenu() {
            if (isMenuOpen) {
                isMenuOpen = false;
                const mobileNav = document.getElementById('mobileNav');
                const menuIcon = document.querySelector('.menu-icon');
                const closeIcon = document.querySelector('.close-icon');

                mobileNav.classList.remove('open');
                menuIcon.style.display = 'block';
                closeIcon.style.display = 'none';
            }
        }

        // Scroll handler
        function handleScroll() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const shouldBeScrolled = scrollTop > 50;

            if (shouldBeScrolled !== isScrolled) {
                isScrolled = shouldBeScrolled;
                const nav = document.getElementById('navigation');
                
                if (isScrolled) {
                    nav.classList.add('scrolled');
                } else {
                    nav.classList.remove('scrolled');
                }
            }
        }

        // Event listeners
        window.addEventListener('scroll', handleScroll);
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {
            const nav = document.getElementById('navigation');
            const mobileNav = document.getElementById('mobileNav');
            
            if (isMenuOpen && !nav.contains(event.target)) {
                closeMobileMenu();
            }
        });

        // Handle window resize
        window.addEventListener('resize', function() {
            if (window.innerWidth > 768 && isMenuOpen) {
                closeMobileMenu();
            }
        });

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            handleScroll();
        });





         // Video play functionality
        // New function name to avoid conflicts
function playVideo() {
    const video = document.getElementById('heroVideo');
    const placeholder = document.getElementById('videoPlaceholder');
    
    if (video) {
        // Hide the placeholder
        placeholder.classList.add('hidden');
        
        // Show and play the video
        video.style.display = 'block';
        video.play();
        
        // Optional: Hide placeholder completely after video starts
        video.addEventListener('play', function() {
            placeholder.style.display = 'none';
        });
        
        // Show placeholder again if video ends
        video.addEventListener('ended', function() {
            placeholder.style.display = 'flex';
            placeholder.classList.remove('hidden');
            video.style.display = 'none';
        });
    }
}

function showComingSoon() {
    alert('Demo reel coming soon! Upload a video through the admin panel.');
}

// Optional: Load video data dynamically via AJAX
function loadHeroVideoData() {
    fetch('/api/hero-video/')
        .then(response => response.json())
        .then(data => {
            if (data.has_video) {
                console.log('Hero video loaded:', data.title);
                // You can update the UI dynamically here if needed
            }
        })
        .catch(error => {
            console.error('Error loading hero video:', error);
        });
}

// Load video data when page loads
document.addEventListener('DOMContentLoaded', loadHeroVideoData);

        // Smooth scrolling for scroll indicator
        document.addEventListener('DOMContentLoaded', function() {
            const scrollIndicator = document.querySelector('.scroll-indicator');
            
            scrollIndicator.addEventListener('click', function() {
                window.scrollTo({
                    top: window.innerHeight,
                    behavior: 'smooth'
                });
            });
        });

        // Add some interactive hover effects
        document.addEventListener('DOMContentLoaded', function() {
            const playButton = document.querySelector('.play-button');
            const videoContainer = document.querySelector('.video-container');
            
            // Add hover effect to video container
            videoContainer.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.02)';
                this.style.transition = 'transform 0.3s ease';
            });
            
            videoContainer.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
            });
            
            // Add click effect to play button
            playButton.addEventListener('mousedown', function() {
                this.style.transform = 'scale(0.95)';
            });
            
            playButton.addEventListener('mouseup', function() {
                this.style.transform = 'scale(1.05)';
            });
        });




        // Portfolio filtering functionality
        document.addEventListener('DOMContentLoaded', function() {
            const filterButtons = document.querySelectorAll('.filter-btn');
            const projectCards = document.querySelectorAll('.project-card');
            
            filterButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const filter = this.getAttribute('data-filter');
                    
                    // Update active button
                    filterButtons.forEach(btn => btn.classList.remove('active'));
                    this.classList.add('active');
                    
                    // Filter projects
                    projectCards.forEach(card => {
                        const category = card.getAttribute('data-category');
                        
                        if (filter === 'all' || category === filter) {
                            card.style.display = 'block';
                            // Add fade-in animation
                            card.style.opacity = '0';
                            setTimeout(() => {
                                card.style.transition = 'opacity 0.3s ease';
                                card.style.opacity = '1';
                            }, 100);
                        } else {
                            card.style.display = 'none';
                        }
                    });
                });
            });
            
            // Add click handlers for project cards
// Global function to close the video modal
function closeVideoModal() {
    const modal = document.getElementById('videoModal');
    if (modal) {
        const video = modal.querySelector('video');
        if (video) {
            video.pause(); // Pause video
        }
        modal.remove();
    }
}

// Open modal and play the selected video
function openVideoModal(videoUrl, title) {
    if (!videoUrl || videoUrl === 'None' || videoUrl.trim() === '') {
        alert('Video file not available.');
        return;
    }

    // Remove existing modal if present
    closeVideoModal();

    const modalHTML = `
        <div class="video-modal" id="videoModal">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>${title}</h3>
                    <button class="close-btn" id="closeModalBtn">&times;</button>
                </div>
                <div class="modal-body">
                    <video controls width="100%" height="300" preload="metadata">
                        <source src="${videoUrl}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    <div class="video-error" style="display: none; color: red; margin-top: 10px;">
                        Error loading video. Please try again.
                    </div>
                </div>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHTML);

    // Add event listeners
    const modal = document.getElementById('videoModal');
    const video = modal.querySelector('video');
    const closeBtn = document.getElementById('closeModalBtn');

    closeBtn.addEventListener('click', closeVideoModal);

    video.addEventListener('error', function () {
        document.querySelector('.video-error').style.display = 'block';
    });

    // Inject modal styles once
    if (!document.getElementById('modal-styles')) {
        const styles = `
            <style id="modal-styles">
                .video-modal {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.8);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 1000;
                }
                .modal-content {
                    background: var(--card, #fff);
                    border-radius: 0.5rem;
                    max-width: 90%;
                    max-height: 90%;
                    overflow: hidden;
                }
                .modal-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 1rem;
                    border-bottom: 1px solid var(--border, #ccc);
                }
                .modal-header h3 {
                    margin: 0;
                    color: var(--foreground, #000);
                }
                .close-btn {
                    background: none;
                    border: none;
                    font-size: 1.5rem;
                    cursor: pointer;
                    color: var(--foreground, #000);
                }
                .close-btn:hover {
                    opacity: 0.7;
                }
                .modal-body {
                    padding: 1rem;
                }
            </style>
        `;
        document.head.insertAdjacentHTML('beforeend', styles);
    }
}

// Main logic (runs after everything has loaded)
window.onload = function () {
    const projectCards = document.querySelectorAll('.project-card');
    const watchButtons = document.querySelectorAll('.watch-btn:not(.disabled)');

    // Redirect to detail page when card is clicked
    projectCards.forEach(card => {
        card.addEventListener('click', function (e) {
            if (e.target.closest('.watch-btn')) return;

            const projectId = this.dataset.projectId;
            if (projectId) {
                window.location.href = `/project/${projectId}/`;
            }
        });
    });

    // Open video modal when watch button is clicked
    watchButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.stopPropagation();
            e.preventDefault();

            const videoUrl = this.dataset.videoUrl;
            const title = this.dataset.projectTitle ||
                this.closest('.project-card').querySelector('.project-title').textContent;

            openVideoModal(videoUrl, title);
        });
    });
};

// Close modal on outside click
document.addEventListener('click', function (e) {
    if (e.target.classList.contains('video-modal')) {
        closeVideoModal();
    }
});

// Close modal on Escape key press
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
        closeVideoModal();
    }
});

            
            // Add click handler for CTA button
            const ctaButton = document.querySelector('.cta-btn');
            ctaButton.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('View Full Portfolio clicked');
                // Add your CTA logic here
            });
        });




        // Animate proficiency bars on scroll
        function animateProficiencyBars() {
            const proficiencyBars = document.querySelectorAll('.proficiency-fill');
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const bar = entry.target;
                        const proficiency = bar.dataset.proficiency;
                        
                        // Animate the bar
                        setTimeout(() => {
                            bar.style.width = proficiency + '%';
                        }, 200);
                        
                        // Unobserve after animation
                        observer.unobserve(bar);
                    }
                });
            }, {
                threshold: 0.5
            });
            
            proficiencyBars.forEach(bar => {
                observer.observe(bar);
            });
        }

        // Add smooth reveal animation for cards
        function addRevealAnimation() {
            const cards = document.querySelectorAll('.card');
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach((entry, index) => {
                    if (entry.isIntersecting) {
                        setTimeout(() => {
                            entry.target.style.opacity = '1';
                            entry.target.style.transform = 'translateY(0)';
                        }, index * 100);
                        
                        observer.unobserve(entry.target);
                    }
                });
            }, {
                threshold: 0.1
            });
            
            cards.forEach(card => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                observer.observe(card);
            });
        }

        // Initialize animations when DOM is loaded
        document.addEventListener('DOMContentLoaded', function() {
            animateProficiencyBars();
            addRevealAnimation();
        });

        // Add hover effects for enhanced interactivity
        document.querySelectorAll('.card').forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-8px)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });





        // Add any interactive functionality here
        document.addEventListener('DOMContentLoaded', function() {
            // Button click handlers
            const downloadBtn = document.querySelector('.btn-hero');
            const chatBtn = document.querySelector('.btn-glass');
            
            downloadBtn.addEventListener('click', function() {
                console.log('Download CV clicked');
                // Add download functionality here
            });
            
            chatBtn.addEventListener('click', function() {
                console.log('Let\'s Chat clicked');
                // Add chat functionality here
            });
            
            // Add hover effects for stat cards
            const statCards = document.querySelectorAll('.stat-card');
            statCards.forEach(card => {
                card.addEventListener('mouseenter', function() {
                    this.style.transform = 'translateY(-5px)';
                });
                
                card.addEventListener('mouseleave', function() {
                    this.style.transform = 'translateY(0)';
                });
            });
        });




        // Form handling
        document.getElementById('contactForm').addEventListener('submit', async function(e) {
            e.preventDefault();

            const formData = new FormData(this);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch('/contact/send/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (result.success) {
                    showToast();
                    this.reset();
                } else {
                    alert("Error: " + result.error);
                }
            } catch (error) {
                alert("Something went wrong. Please try again.");
                console.error(error);
            }
        });


        function showToast() {
            const toast = document.getElementById('toast');
            toast.classList.add('show');
            
            // Hide toast after 3 seconds
            setTimeout(() => {
                toast.classList.remove('show');
            }, 3000);
        }

        // Add smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            });
        });

        // Add form validation feedback
        const inputs = document.querySelectorAll('.form-input, .form-textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.value.trim() === '' && this.hasAttribute('required')) {
                    this.style.borderColor = 'hsl(0, 72%, 51%)';
                } else {
                    this.style.borderColor = 'hsl(220, 13%, 20%)';
                }
            });
            
            input.addEventListener('input', function() {
                if (this.style.borderColor === 'hsl(0, 72%, 51%)' && this.value.trim() !== '') {
                    this.style.borderColor = 'hsl(220, 13%, 20%)';
                }
            });
        });



        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        const csrftoken = getCookie('csrftoken');
