// Initialize AOS
AOS.init({
    duration: 1000,
    once: true,
    offset: 100
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Navbar color change on scroll
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(0, 0, 0, 0.9)';
    } else {
        navbar.style.background = 'rgba(0, 0, 0, 0.7)';
    }
});

// Newsletter subscription form handling
document.addEventListener('DOMContentLoaded', function() {
    const subscribeForm = document.getElementById('subscribeForm');
    if (subscribeForm) {
        subscribeForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const emailInput = this.querySelector('input[type="email"]');
            const feedbackDiv = document.querySelector('.form-feedback');
            const submitButton = this.querySelector('button[type="submit"]');

            // Email validation regex
            const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

            if (!emailRegex.test(emailInput.value)) {
                feedbackDiv.textContent = 'Please enter a valid email address';
                feedbackDiv.style.display = 'block';
                feedbackDiv.style.color = '#dc3545';
                emailInput.classList.add('is-invalid');
                return;
            }

            // Disable form while submitting
            submitButton.disabled = true;
            emailInput.disabled = true;

            try {
                const formData = new FormData();
                formData.append('email', emailInput.value);

                const response = await fetch('/subscribe', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                feedbackDiv.style.display = 'block';

                if (data.success) {
                    feedbackDiv.style.color = '#28a745';
                    feedbackDiv.textContent = data.message;
                    subscribeForm.reset();
                } else {
                    feedbackDiv.style.color = '#dc3545';
                    feedbackDiv.textContent = data.message;
                }
            } catch (error) {
                console.error('Error:', error);
                feedbackDiv.style.color = '#dc3545';
                feedbackDiv.style.display = 'block';
                feedbackDiv.textContent = 'There was an error processing your subscription. Please try again later.';
            } finally {
                // Re-enable form
                submitButton.disabled = false;
                emailInput.disabled = false;
            }
        });
    }
});

// Parallax effect for hero section
window.addEventListener('scroll', function() {
    const hero = document.querySelector('.hero');
    const scrolled = window.pageYOffset;
    hero.style.backgroundPositionY = (scrolled * 0.5) + 'px';
});

// Mobile menu close on click
document.querySelectorAll('.navbar-nav>li>a').forEach(link => {
    link.addEventListener('click', () => {
        const navbarCollapse = document.querySelector('.navbar-collapse');
        if (navbarCollapse.classList.contains('show')) {
            navbarCollapse.classList.remove('show');
        }
    });
});
