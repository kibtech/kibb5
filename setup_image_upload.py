#!/usr/bin/env python3
"""
Setup Image Upload for Cyber Services
=====================================
Set up image upload functionality for cyber services.
"""

import os
import sys

def create_image_upload_endpoint():
    """Create the backend endpoint for image uploads"""
    
    upload_endpoint_code = '''
# Add this to app/admin/cyber_services.py (or create new file)

import os
import uuid
from werkzeug.utils import secure_filename
from flask import request, jsonify, current_app, url_for
from flask_jwt_extended import jwt_required
from PIL import Image
import io

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def optimize_image(image_data, max_size=(800, 600), quality=85):
    """Optimize image for web use"""
    try:
        # Open image
        img = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if necessary (for JPEG)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Resize if larger than max_size
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save optimized image
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        return output.getvalue()
    except Exception as e:
        print(f"Error optimizing image: {e}")
        return image_data

@bp.route('/upload-image', methods=['POST'])
@jwt_required()
def upload_cyber_service_image():
    """Upload and optimize image for cyber service"""
    try:
        # Check if file is present
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, WEBP'}), 400
        
        # Create uploads directory if it doesn't exist
        upload_dir = os.path.join(current_app.root_path, '..', 'static', 'uploads', 'cyber-services')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        
        # Read and optimize image
        image_data = file.read()
        
        # Check file size (max 5MB)
        if len(image_data) > 5 * 1024 * 1024:
            return jsonify({'error': 'File too large. Maximum size is 5MB'}), 400
        
        # Optimize image
        optimized_data = optimize_image(image_data)
        
        # Save optimized image
        file_path = os.path.join(upload_dir, unique_filename)
        with open(file_path, 'wb') as f:
            f.write(optimized_data)
        
        # Generate URL for the uploaded image
        image_url = f"/static/uploads/cyber-services/{unique_filename}"
        
        return jsonify({
            'success': True,
            'message': 'Image uploaded successfully',
            'image_url': image_url,
            'filename': unique_filename
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/delete-image', methods=['DELETE'])
@jwt_required()
def delete_cyber_service_image():
    """Delete uploaded cyber service image"""
    try:
        data = request.get_json()
        filename = data.get('filename')
        
        if not filename:
            return jsonify({'error': 'Filename is required'}), 400
        
        # Security check - ensure filename is safe
        safe_filename = secure_filename(filename)
        if safe_filename != filename:
            return jsonify({'error': 'Invalid filename'}), 400
        
        # Construct file path
        file_path = os.path.join(current_app.root_path, '..', 'static', 'uploads', 'cyber-services', filename)
        
        # Delete file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'success': True, 'message': 'Image deleted successfully'}), 200
        else:
            return jsonify({'error': 'Image not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
'''
    
    return upload_endpoint_code

def create_static_file_serving():
    """Create static file serving configuration"""
    
    static_config = '''
# Add this to your main Flask app configuration (app/__init__.py or run.py)

import os
from flask import Flask, send_from_directory

def create_app():
    app = Flask(__name__)
    
    # ... your existing configuration ...
    
    # Serve uploaded files
    @app.route('/static/uploads/<path:filename>')
    def uploaded_file(filename):
        upload_dir = os.path.join(app.root_path, '..', 'static', 'uploads')
        return send_from_directory(upload_dir, filename)
    
    return app

# Alternative: Add to your main routes file
@app.route('/static/uploads/<path:filename>')
def uploaded_file(filename):
    upload_dir = os.path.join(current_app.root_path, '..', 'static', 'uploads')
    return send_from_directory(upload_dir, filename)
'''
    
    return static_config

def create_frontend_upload_component():
    """Create the frontend upload component"""
    
    upload_component = '''
// Add this to your AdminCyberServicesPage.js

const [uploadingImage, setUploadingImage] = useState(false);
const [uploadError, setUploadError] = useState('');

const handleImageUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  
  // Validate file type
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
  if (!allowedTypes.includes(file.type)) {
    setUploadError('Invalid file type. Please select JPG, PNG, GIF, or WEBP image.');
    return;
  }
  
  // Validate file size (5MB)
  if (file.size > 5 * 1024 * 1024) {
    setUploadError('File too large. Maximum size is 5MB.');
    return;
  }
  
  setUploadingImage(true);
  setUploadError('');
  
  try {
    const formData = new FormData();
    formData.append('image', file);
    
    const response = await fetch('/api/admin/cyber-services/upload-image', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('adminToken')}`
      },
      body: formData
    });
    
    const data = await response.json();
    
    if (response.ok) {
      // Update form data with new image URL
      setFormData(prev => ({
        ...prev,
        image_url: data.image_url
      }));
      toast.success('Image uploaded successfully!');
    } else {
      setUploadError(data.error || 'Failed to upload image');
    }
  } catch (error) {
    setUploadError('Error uploading image');
    console.error('Upload error:', error);
  } finally {
    setUploadingImage(false);
  }
};

// Add this to your form JSX (replace the existing image URL input):

<div>
  <label className="block text-sm font-medium text-gray-700 mb-1">
    Service Image
  </label>
  
  {/* Image Upload Section */}
  <div className="space-y-3">
    {/* File Upload */}
    <div>
      <input
        type="file"
        accept="image/jpeg,image/jpg,image/png,image/gif,image/webp"
        onChange={handleImageUpload}
        disabled={uploadingImage}
        className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 disabled:opacity-50"
      />
      <p className="text-xs text-gray-500 mt-1">
        Upload JPG, PNG, GIF, or WEBP. Max size: 5MB. Images will be optimized automatically.
      </p>
    </div>
    
    {/* OR Divider */}
    <div className="flex items-center">
      <div className="flex-grow border-t border-gray-300"></div>
      <span className="px-3 text-xs text-gray-500 bg-white">OR</span>
      <div className="flex-grow border-t border-gray-300"></div>
    </div>
    
    {/* URL Input */}
    <div>
      <input
        type="url"
        name="image_url"
        value={formData.image_url}
        onChange={handleInputChange}
        placeholder="https://example.com/image.jpg"
        className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <p className="text-xs text-gray-500 mt-1">
        Or enter a direct image URL
      </p>
    </div>
  </div>
  
  {/* Upload Status */}
  {uploadingImage && (
    <div className="mt-2 text-sm text-blue-600">
      <div className="flex items-center">
        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
        Uploading and optimizing image...
      </div>
    </div>
  )}
  
  {uploadError && (
    <div className="mt-2 text-sm text-red-600">
      {uploadError}
    </div>
  )}
  
  {/* Image Preview */}
  {formData.image_url && (
    <div className="mt-3">
      <p className="text-xs text-gray-600 mb-2">Preview:</p>
      <div className="relative">
        <img
          src={formData.image_url}
          alt="Service preview"
          className="w-48 h-32 object-cover rounded-lg border"
          onError={(e) => {
            e.target.style.display = 'none';
            e.target.nextSibling.style.display = 'block';
          }}
        />
        <div className="w-48 h-32 bg-gray-100 rounded-lg border flex items-center justify-center text-xs text-gray-500" style={{display: 'none'}}>
          Invalid image
        </div>
        {/* Remove Image Button */}
        <button
          type="button"
          onClick={() => setFormData(prev => ({ ...prev, image_url: '' }))}
          className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs hover:bg-red-600"
        >
          ×
        </button>
      </div>
    </div>
  )}
</div>
'''
    
    return upload_component

if __name__ == "__main__":
    print("🖼️ Setting Up Image Upload for Cyber Services")
    print("=" * 50)
    
    print("\n1. 🔧 Backend Upload Endpoint:")
    print("=" * 30)
    print(create_image_upload_endpoint())
    
    print("\n2. 📁 Static File Serving:")
    print("=" * 30)
    print(create_static_file_serving())
    
    print("\n3. 📱 Frontend Upload Component:")
    print("=" * 30)
    print(create_frontend_upload_component())
    
    print("\n✅ IMPLEMENTATION SUMMARY:")
    print("=" * 30)
    print("🎯 FEATURES INCLUDED:")
    print("• Direct file upload (drag & drop)")
    print("• Image optimization (resize, compress)")
    print("• File type validation (JPG, PNG, GIF, WEBP)")
    print("• File size limit (5MB)")
    print("• Live preview")
    print("• URL input as alternative")
    print("• Error handling")
    print("• Image deletion")
    print()
    print("🔧 SETUP STEPS:")
    print("1. Add upload endpoint to admin routes")
    print("2. Configure static file serving")
    print("3. Update frontend component")
    print("4. Create uploads directory")
    print("5. Install Pillow for image processing: pip install Pillow")