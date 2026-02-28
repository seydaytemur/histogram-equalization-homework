# Histogram Eşitleme (Histogram Equalization) - Python

Bu proje, görüntü işleme dersi ödevi kapsamında geliştirilmiş, **hiçbir hazır histogram eşitleme (örneğin OpenCV'nin `cv2.equalizeHist()` gibi) fonksiyonu kullanılmadan**, tamamen sıfırdan matematiksel algoritmalarla (Kümülatif Dağılım Fonksiyonu - CDF) yazılmış bir histogram eşitleme scriptidir.

## Proje Hakkında

Algoritma, düşük kontrastlı (soluk, üzerine gri sis inmiş gibi görünen) fotoğrafların kontrastını artırmak için kullanılır. Dar bir aralığa sıkışmış olan piksel yoğunluk değerlerini, 0-255 (tam siyah - tam beyaz) arasındaki tüm renk skalasına homojen bir şekilde yayar.

### Adım Adım Çalışma Mantığı:
1.  **Histogram Çıkarımı:** Görüntüdeki her bir piksel değerinden (0-255 arası) kaç tane olduğu 256 elemanlı bir dizide sayılır.
2.  **CDF (Kümülatif Dağılım Fonksiyonu):** Piksel sayılarının yığılımlı toplamı alınır.
3.  **Normalizasyon:** Bulunan CDF değerleri `((CDF - CDF_min) / (Toplam Piksel - CDF_min)) * 255` matematiksel formülü ile yeni bir renk uzayına (mapping) haritalandırılır.
4.  **Uygulama:** Orijinal kısıtlı pikseller, yeni hesaplanan bu geniş, eşitlenmiş pikseller ile değiştirilir.

## Kullanılan Teknolojiler
- **Python 3.x**
- **NumPy** (Yalnızca matris işlemleri ve diziler için)
- **OpenCV (`cv2`)** (Yalnızca resmi okumak için - IMREAD_GRAYSCALE)
- **Matplotlib** (Eski/Yeni görüntüleri ve grafiklerini çizdirmek için)


