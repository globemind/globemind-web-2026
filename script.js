// Navigation scroll effect
const navbar = document.getElementById('navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
    
    lastScroll = currentScroll;
});

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            const headerOffset = 80;
            const elementPosition = targetElement.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });

            // Close mobile menu if open
            const navLinks = document.querySelector('.nav-links');
            const mobileMenuToggle = document.getElementById('mobileMenuToggle');
            if (navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                mobileMenuToggle.classList.remove('active');
            }
        }
    });
});

// Mobile menu toggle
const mobileMenuToggle = document.getElementById('mobileMenuToggle');
const navLinks = document.querySelector('.nav-links');

if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        mobileMenuToggle.classList.toggle('active');
    });
}

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            // Stop observing once animated
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all fade-in elements
document.querySelectorAll('.fade-in').forEach(el => {
    observer.observe(el);
});

// Counter animation for statistics
const animateCounter = (element, target, duration = 2000) => {
    const start = 0;
    const increment = target / (duration / 16); // 60fps
    let current = start;

    const updateCounter = () => {
        current += increment;
        if (current < target) {
            element.textContent = Math.floor(current);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    };

    updateCounter();
};

// Observe statistics section for counter animation
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const statItems = entry.target.querySelectorAll('.stat-item');
            statItems.forEach(item => {
                const numberElement = item.querySelector('.stat-number');
                const target = parseInt(numberElement.getAttribute('data-target'));
                
                if (target && !numberElement.classList.contains('animated')) {
                    numberElement.classList.add('animated');
                    animateCounter(numberElement, target);
                }
            });
            // Stop observing once animated
            statsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

const statisticsSection = document.querySelector('.statistics');
if (statisticsSection) {
    statsObserver.observe(statisticsSection);
}

// Contact form handling
const contactForm = document.getElementById('contactForm');
const formMessage = document.getElementById('formMessage');

if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(contactForm);
        const data = Object.fromEntries(formData);
        
        // Basic validation
        const requiredFields = ['name', 'email', 'service', 'message'];
        let isValid = true;
        
        requiredFields.forEach(field => {
            const input = contactForm.querySelector(`[name="${field}"]`);
            if (!data[field] || data[field].trim() === '') {
                isValid = false;
                input.style.borderColor = '#dc3545';
            } else {
                input.style.borderColor = '#dfdfdf';
            }
        });
        
        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (data.email && !emailRegex.test(data.email)) {
            isValid = false;
            contactForm.querySelector('[name="email"]').style.borderColor = '#dc3545';
        }
        
        if (!isValid) {
            formMessage.textContent = 'Por favor, completa todos los campos requeridos correctamente.';
            formMessage.className = 'form-message error';
            return;
        }
        
        // Simulate form submission
        formMessage.textContent = '¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.';
        formMessage.className = 'form-message success';
        
        // Reset form
        contactForm.reset();
        
        // Clear message after 5 seconds
        setTimeout(() => {
            formMessage.className = 'form-message';
            formMessage.textContent = '';
        }, 5000);
        
        // In a real implementation, you would send the data to a server here
        console.log('Form data:', data);
    });
    
    // Clear error states on input
    contactForm.querySelectorAll('input, select, textarea').forEach(input => {
        input.addEventListener('input', () => {
            input.style.borderColor = '#dfdfdf';
            if (formMessage.classList.contains('error')) {
                formMessage.className = 'form-message';
                formMessage.textContent = '';
            }
        });
    });
}

// Add smooth scroll offset for fixed header
document.querySelectorAll('section[id]').forEach(section => {
    section.style.scrollMarginTop = '80px';
});

// Performance optimization: Lazy load animations
const lazyAnimate = () => {
    const elements = document.querySelectorAll('.fade-in:not(.visible)');
    elements.forEach(el => {
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight + 100) {
            el.classList.add('visible');
        }
    });
};

// Initial check for elements in viewport
lazyAnimate();

// Throttled scroll listener for performance
let ticking = false;
window.addEventListener('scroll', () => {
    if (!ticking) {
        window.requestAnimationFrame(() => {
            lazyAnimate();
            ticking = false;
        });
        ticking = true;
    }
});

// Add active state to navigation links based on scroll position
const updateActiveNavLink = () => {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (window.pageYOffset >= sectionTop - 100) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
};

window.addEventListener('scroll', updateActiveNavLink);
updateActiveNavLink(); // Initial call

