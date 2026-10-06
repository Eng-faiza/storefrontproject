const API_BASE_URL = 'http://127.0.0.1:8000';
const PRODUCTS_URL = `${API_BASE_URL}/store/products/`;

const uploadForm = document.querySelector('#upload-form');
const productIdInput = document.querySelector('#product-id');
const imageInput = document.querySelector('#image-input');
const uploadButton = document.querySelector('#upload-button');
const statusMessage = document.querySelector('#status');
const preview = document.querySelector('#preview');
const previewImage = document.querySelector('#preview-image');
const productsList = document.querySelector('#products-list');
const refreshButton = document.querySelector('#refresh-button');

imageInput.addEventListener('change', () => {
  const [file] = imageInput.files;
  if (!file) {
    preview.hidden = true;
    return;
  }

  previewImage.src = URL.createObjectURL(file);
  preview.hidden = false;
});

uploadForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const [file] = imageInput.files;
  const productId = productIdInput.value;

  if (!file || !productId) {
    setStatus('Choose an image and enter a product ID.', 'error');
    return;
  }

  const formData = new FormData();
  formData.append('image', file);
  uploadButton.disabled = true;
  setStatus('Uploading...', 'loading');

  try {
    const response = await fetch(`${PRODUCTS_URL}${productId}/images/`, {
      method: 'POST',
      body: formData,
    });

    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(formatApiError(data, response.status));
    }

    setStatus('Image uploaded successfully.', 'success');
    uploadForm.reset();
    preview.hidden = true;
    loadProducts();
  } catch (error) {
    setStatus(error.message || 'Upload failed. Check that Django is running.', 'error');
  } finally {
    uploadButton.disabled = false;
  }
});

refreshButton.addEventListener('click', loadProducts);

async function loadProducts() {
  productsList.innerHTML = '<p class="muted">Loading products...</p>';

  try {
    const response = await fetch(PRODUCTS_URL);
    if (!response.ok) {
      throw new Error(`Could not load products (${response.status}).`);
    }

    const payload = await response.json();
    const products = Array.isArray(payload) ? payload : payload.results || [];
    renderProducts(products);
  } catch (error) {
    productsList.innerHTML = `<p class="error-text">${escapeHtml(error.message)}</p>`;
  }
}

function renderProducts(products) {
  if (!products.length) {
    productsList.innerHTML = '<p class="muted">No products found.</p>';
    return;
  }

  productsList.innerHTML = products.map((product) => {
    const image = product.images && product.images[0];
    const imageUrl = image && image.image ? image.image : '';
    return `
      <article class="product-card">
        ${imageUrl ? `<img src="${imageUrl}" alt="${escapeHtml(product.title)}">` : '<div class="image-placeholder">No image</div>'}
        <div>
          <span class="product-id">#${product.id}</span>
          <h3>${escapeHtml(product.title)}</h3>
          <p>${product.unit_price} &middot; ${product.inventory} in stock</p>
        </div>
      </article>
    `;
  }).join('');
}

function formatApiError(data, status) {
  if (data.image && Array.isArray(data.image)) return data.image.join(' ');
  if (data.detail) return data.detail;
  return `Upload failed (${status}).`;
}

function setStatus(message, state) {
  statusMessage.textContent = message;
  statusMessage.className = `status ${state}`;
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, (character) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;',
  }[character]));
}

loadProducts();
