document.getElementsByClassName('md-header__title')[0].onclick = function() { location.href = document.location.origin }

// Enable caching for static assets (images, CSS, JS) while preventing HTML caching
var head = document.getElementsByTagName('head')[0];
[
  { httpEquiv: 'cache-control', content: 'no-cache, must-revalidate, post-check=0, pre-check=0' },
  { httpEquiv: 'expires', content: '0' },
  { httpEquiv: 'pragma', content: 'no-cache' }
].forEach(metaData => {
  var meta = document.createElement('meta');
  meta.httpEquiv = metaData.httpEquiv;
  meta.content = metaData.content;
  head.appendChild(meta);
});

document.addEventListener("DOMContentLoaded", function() {
    // Lazy loading for images
    const images = document.querySelectorAll('img');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src || img.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    }, {
        rootMargin: '50px 0px',
        threshold: 0.01
    });

    images.forEach(img => {
        if (img.src) {
            img.dataset.src = img.src;
            img.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMSIgaGVpZ2h0PSIxIiB2aWV3Qm94PSIwIDAgMSAxIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxyZWN0IHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiNmNWY1ZjUiLz48L3N2Zz4=';
            img.classList.add('lazy');
            imageObserver.observe(img);
        }
    });

    const content = document.querySelector(".md-content");
    const items = Array.from(content.querySelectorAll(".item"));
    const chunkSize = 20;
    let loaded = chunkSize;

    // Hide items initially
    items.forEach((item, i) => {
        if (i >= loaded) item.style.display = "none";
    });

    // Load more on scroll
    window.addEventListener("scroll", () => {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 50) {
            const nextItems = items.slice(loaded, loaded + chunkSize);
            nextItems.forEach(item => item.style.display = "block");
            loaded += chunkSize;
        }
    });
});