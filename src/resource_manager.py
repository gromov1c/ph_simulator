"""
Resource Manager for the pH Calculator Application.
Handles proper resource cleanup to prevent memory leaks and improve performance.
"""
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPixmap, QPixmapCache


class ResourceManager(QObject):
    """
    Manages resources like images, animations, and signal connections
    to ensure proper cleanup when the app is closed.
    """
    cleanup_complete = Signal()
    
    def __init__(self):
        super().__init__()
        self._image_cache = {}
        self._connections = []
        
        # Configure application-wide pixmap cache (50MB)
        QPixmapCache.setCacheLimit(50000)
    
    def cache_image(self, path, pixmap):
        """Cache a scaled image to avoid repeated scaling operations."""
        self._image_cache[path] = pixmap
        return pixmap
    
    def get_cached_image(self, path):
        """Get an image from the cache, or None if not cached."""
        return self._image_cache.get(path)
    
    def track_connection(self, obj, signal, slot):
        """Track a signal-slot connection for later disconnection."""
        # Connect the signal and slot
        getattr(obj, signal).connect(slot)
        # Store the connection info
        self._connections.append((obj, signal, slot))
        
    def cleanup(self):
        """Clean up all tracked resources."""
        # Disconnect all tracked connections
        for obj, signal, slot in self._connections:
            try:
                getattr(obj, signal).disconnect(slot)
            except (RuntimeError, TypeError):
                # Connection may already be broken, ignore
                pass
        
        # Clear the image cache
        self._image_cache.clear()
        
        # Emit signal that cleanup is complete
        self.cleanup_complete.emit() 