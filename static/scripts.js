document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in
    fetch('/images')
        .then(response => response.json())
        .then(data => {
            if (data.success === false && data.message === "User not logged in") {
                document.getElementById('authContainer').classList.remove('d-none');
            } else {
                document.getElementById('mainApp').classList.remove('d-none');
                loadImages();
            }
        })
        .catch(error => console.error('Error:', error));

    document.getElementById('loginForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;
        
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('authContainer').classList.add('d-none');
                document.getElementById('mainApp').classList.remove('d-none');
                loadImages();
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    });

    document.getElementById('signupForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const username = document.getElementById('signupUsername').value;
        const password = document.getElementById('signupPassword').value;
        
        fetch('/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('User registered successfully. Please log in.');
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    });

    document.getElementById('logoutButton').addEventListener('click', function() {
        fetch('/logout', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('mainApp').classList.add('d-none');
                    document.getElementById('authContainer').classList.remove('d-none');
                }
            })
            .catch(error => console.error('Error:', error));
    });

    document.getElementById('imageInput').addEventListener('change', function() {
        const formData = new FormData();
        formData.append('image', document.getElementById('imageInput').files[0]);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadImages();
            } else {
                alert('Image upload failed');
            }
        })
        .catch(error => console.error('Error:', error));
    });
});

function loadImages() {
    fetch('/images')
        .then(response => response.json())
        .then(data => {
            const imagesContainer = document.getElementById('imagesContainer');
            imagesContainer.innerHTML = '';
            data.images.forEach(image => {
                const col = document.createElement('div');
                col.className = 'col-12 col-sm-6 col-md-4 col-lg-3 mb-4';
                const imageCard = document.createElement('div');
                imageCard.className = 'imageCard';
                imageCard.innerHTML = `
                    <img src="${image.image_url}" alt="User Image">
                    <button onclick="likeImage(${image.id})" id="like-btn-${image.id}">Like (${image.likes})</button>
                `;
                col.appendChild(imageCard);
                imagesContainer.appendChild(col);
            });
        })
        .catch(error => console.error('Error:', error));
}

function likeImage(imageId) {
    fetch(`/like/${imageId}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update the like count for the specific image
                const likeButton = document.getElementById(`like-btn-${imageId}`);
                const currentLikes = parseInt(likeButton.innerText.match(/\d+/)[0], 10);
                likeButton.innerText = `Like (${currentLikes + 1})`;
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
}
