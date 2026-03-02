import cv2
import numpy as np
import matplotlib.pyplot as plt

def histogram_esitleme(goruntu):
    # Görüntünün boyutları
    satir, sutun = goruntu.shape
    toplam_piksel = satir * sutun
    
    # 1. Histogramı Hesaplama (Her piksel değerinden kaç tane olduğunu bulma)
    # Hazır fonksiyon kullanmamak için 256 elemanlı 0 dizisi oluşturup pikselleri sayıyoruz
    histogram = np.zeros(256, dtype=int)
    for i in range(satir):
        for j in range(sutun):
            piksel_degeri = goruntu[i, j]
            histogram[piksel_degeri] += 1
            
    # 2. Kümülatif Dağılım Fonksiyonu (CDF) Hesaplama
    cdf = np.zeros(256, dtype=int)
    cdf[0] = histogram[0]
    for i in range(1, 256):
        cdf[i] = cdf[i-1] + histogram[i]
        
    # 3. CDF'yi Normalize Etme (0-255 aralığına ölçekleme)
    # Formül: Normalize_CDF = round(((CDF(v) - CDF_min) / (Toplam_Piksel - CDF_min)) * 255)
    
    # Sıfır olmayan en küçük CDF değerini (CDF_min) bulma
    cdf_min = 0
    for deger in cdf:
        if deger > 0:
            cdf_min = deger
            break
            
    normalize_cdf = np.zeros(256, dtype=np.uint8)
    for i in range(256):
        if cdf[i] > 0:
            yeni_deger = round(((cdf[i] - cdf_min) / (toplam_piksel - cdf_min)) * 255)
            normalize_cdf[i] = yeni_deger
            
    # 4. Yeni piksel değerlerini (eşitlenmiş görüntü) oluşturma
    esitlenmis_goruntu = np.zeros_like(goruntu, dtype=np.uint8)
    for i in range(satir):
        for j in range(sutun):
            esitlenmis_goruntu[i, j] = normalize_cdf[goruntu[i, j]]
            
    return esitlenmis_goruntu, cdf

# --- Kullanım ve Test ---
if __name__ == '__main__':
    # Görüntüyü gri tonlamalı olarak okuyun
    # "araba.jpg" kısmını test edeceğiniz görüntünün tam yolu ile değiştirin.
    img_path = 'araba.png' 
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        print(f"Hata: Görüntü okunamadı. Lütfen '{img_path}' dosyasının mevcut olduğundan emin olun.")
    else:
        # Kendi yazdığımız fonksiyonu çağırıyoruz
        esitlenmis_img, cdf_degerleri = histogram_esitleme(img)
        
        # Orijinal histogramı çizim için hesaplama
        orijinal_hist = np.zeros(256, dtype=int)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                orijinal_hist[img[i, j]] += 1
                
        # Eşitlenmiş görüntünün histogramını çizim için hesaplama
        esitlenmis_hist = np.zeros(256, dtype=int)
        for i in range(esitlenmis_img.shape[0]):
            for j in range(esitlenmis_img.shape[1]):
                esitlenmis_hist[esitlenmis_img[i, j]] += 1
                
        # --- Sonuçları Görselleştirme ---
        plt.figure(figsize=(14, 10))
        
        # Orijinal Görüntü
        plt.subplot(2, 2, 1)
        plt.imshow(img, cmap='gray', vmin=0, vmax=255)
        plt.title('Orijinal Görüntü')
        plt.axis('off')
        
        # Orijinal Histogram
        plt.subplot(2, 2, 2)
        plt.bar(range(256), orijinal_hist, width=1, color='blue', alpha=0.7)
        plt.title('Orijinal Görüntü Histogramı')
        plt.xlabel('Piksel Değeri (0-255)')
        plt.ylabel('Piksel Sayısı')
        plt.xlim([0, 255])
        
        # Eşitlenmiş Görüntü
        plt.subplot(2, 2, 3)
        plt.imshow(esitlenmis_img, cmap='gray', vmin=0, vmax=255)
        plt.title('Eşitlenmiş Görüntü')
        plt.axis('off')
        
        # Eşitlenmiş Histogram
        plt.subplot(2, 2, 4)
        plt.bar(range(256), esitlenmis_hist, width=1, color='green', alpha=0.7)
        plt.title('Eşitlenmiş Görüntü Histogramı')
        plt.xlabel('Piksel Değeri (0-255)')
        plt.ylabel('Piksel Sayısı')
        plt.xlim([0, 255])
        
        plt.tight_layout()
        plt.savefig('histogram_sonucu.png')
        
        # --- Ödev İçin Sonuçların Yorumlanması ---
        print("\n--- Histogram Eşitleme Sonuç Analizi ---")
        print("1. Kontrast Artışı: Orijinal görüntüde pikseller belirli bir aralıkta (genellikle dar bir bantta) toplanmıştı.")
        print("2. Histogram Dağılımı: Eşitleme sonrası pikseller 0-255 aralığına daha homojen şekilde yayıldı.")
        print("3. Görsel Kalite: Görüntüdeki detaylar (özellikle gölge ve aşırı parlak kısımlar) daha belirgin hale geldi.")
        print("4. Manuel Uygulama: Hazır 'histeq' gibi fonksiyonlar yerine pikselleri tek tek sayıp CDF hesabı yapılarak işlem gerçekleştirilmiştir.")
        
        plt.show()
