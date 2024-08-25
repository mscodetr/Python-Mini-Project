import tkinter as tk  # Tkinter modülünü import ediyoruz. Bu, Python'un GUI oluşturma kütüphanesidir.
from PIL import Image, \
    ImageTk  # Pillow (PIL) kütüphanesinden Image ve ImageTk sınıflarını kullanıyoruz. Görselleri yüklemek ve Tkinter ile kullanmak için gerekli.

# Telefon rehberi uygulaması için boş bir rehber oluşturuyoruz.
rehber = {}


# Kişi ekleme fonksiyonu
def kisi_ekle():
    # Kullanıcının giriş alanlarına girdiği isim ve telefon numarasını alıyoruz.
    isim = entry_isim.get()
    telefon = entry_telefon.get()

    # Eğer isim ve telefon alanları doluysa:
    if isim and telefon:
        rehber[isim] = telefon  # Rehbere ismi ve telefon numarasını ekliyoruz.
        mesaj.set(f"{isim} rehbere eklendi.")  # Kullanıcıya bir mesaj gösteriyoruz.
        entry_isim.delete(0, tk.END)  # İsim giriş alanını temizliyoruz.
        entry_telefon.delete(0, tk.END)  # Telefon numarası giriş alanını temizliyoruz.
        liste_guncelle()  # Listeyi güncellemek için fonksiyonu çağırıyoruz.
    else:
        # Eğer giriş alanları boşsa, kullanıcıya uyarı mesajı veriyoruz.
        mesaj.set("Lütfen isim ve telefon numarasını girin.")


# Kişi silme fonksiyonu
def kisi_sil():
    isim = entry_isim.get()  # Kullanıcının giriş alanına yazdığı ismi alıyoruz.

    # Eğer isim rehberde varsa:
    if isim in rehber:
        del rehber[isim]  # Rehberden o ismi siliyoruz.
        mesaj.set(f"{isim} rehberden silindi.")  # Silindiğini belirten bir mesaj gösteriyoruz.
        liste_guncelle()  # Listeyi güncellemek için fonksiyonu çağırıyoruz.
    else:
        # Eğer isim rehberde yoksa, uyarı mesajı gösteriyoruz.
        mesaj.set("Kişi rehberde bulunamadı.")


# Rehberi güncelleme fonksiyonu
def liste_guncelle():
    listbox.delete(0, tk.END)  # Listbox içeriğini temizliyoruz.
    for isim, telefon in rehber.items():  # Rehberdeki tüm isim ve telefonları döngü ile alıyoruz.
        # İsim ve telefon numaralarını listbox'a ekliyoruz.
        listbox.insert(tk.END, f"{isim}: {telefon}")


# Ana pencereyi oluşturuyoruz
pencere = tk.Tk()
pencere.title("Telefon Rehberi Uygulaması")  # Pencerenin başlığını belirliyoruz.
pencere.geometry("400x400")  # Pencerenin boyutlarını belirliyoruz.

# İkon ekleme (ikon dosyası varsa eklenebilir, şimdilik bu satır boş)
# pencere.iconphoto(False, tk.PhotoImage(file='icon.png'))

# Üst resim (banner)
banner_image = Image.open("banner.png")  # banner.png adlı resmi açıyoruz.
banner_image = banner_image.resize((400, 100), Image.Resampling.LANCZOS)  # Resmi belirli boyutlara küçültüyoruz.
banner_photo = ImageTk.PhotoImage(banner_image)  # Resmi Tkinter için uygun formata dönüştürüyoruz.
banner_label = tk.Label(pencere, image=banner_photo)  # Pencereye banner resmi ekliyoruz.
banner_label.grid(row=0, columnspan=2)  # Banner'ı 0. satıra ve 2 sütun genişliğinde yerleştiriyoruz.

# İsim etiketi ve giriş kutusu
label_isim = tk.Label(pencere, text="İsim:")  # İsim için bir etiket oluşturuyoruz.
label_isim.grid(row=1, column=0, pady=5)  # Etiketi 1. satırda ve 0. sütunda yerleştiriyoruz.

entry_isim = tk.Entry(pencere)  # Kullanıcının isim girmesi için bir giriş kutusu oluşturuyoruz.
entry_isim.grid(row=1, column=1, pady=5)  # Giriş kutusunu 1. satırda ve 1. sütunda yerleştiriyoruz.

# Telefon etiketi ve giriş kutusu
label_telefon = tk.Label(pencere, text="Telefon:")  # Telefon için bir etiket oluşturuyoruz.
label_telefon.grid(row=2, column=0, pady=5)  # Etiketi 2. satırda ve 0. sütunda yerleştiriyoruz.

entry_telefon = tk.Entry(pencere)  # Kullanıcının telefon numarası girmesi için bir giriş kutusu oluşturuyoruz.
entry_telefon.grid(row=2, column=1, pady=5)  # Giriş kutusunu 2. satırda ve 1. sütunda yerleştiriyoruz.

# PNG resimlerini butonlara ekleme
add_image = Image.open("add_icon.png")  # Ekleme butonu için add_icon.png resmini açıyoruz.
add_image = add_image.resize((30, 30), Image.Resampling.LANCZOS)  # Buton resmi boyutunu ayarlıyoruz.
add_photo = ImageTk.PhotoImage(add_image)  # Resmi Tkinter formatına dönüştürüyoruz.

delete_image = Image.open("delete_icon.png")  # Silme butonu için delete_icon.png resmini açıyoruz.
delete_image = delete_image.resize((30, 30), Image.Resampling.LANCZOS)  # Buton resmi boyutunu ayarlıyoruz.
delete_photo = ImageTk.PhotoImage(delete_image)  # Resmi Tkinter formatına dönüştürüyoruz.

# Şeffaf görünümlü butonlar (text ve relief kaldırıldı)
button_ekle = tk.Button(pencere, image=add_photo, command=kisi_ekle,
                        bd=0)  # Ekle butonu oluşturuyoruz ve şeffaf yapıyoruz.
button_ekle.grid(row=3, column=0, pady=5)  # Ekle butonunu 3. satır ve 0. sütuna yerleştiriyoruz.

button_sil = tk.Button(pencere, image=delete_photo, command=kisi_sil,
                       bd=0)  # Sil butonu oluşturuyoruz ve şeffaf yapıyoruz.
button_sil.grid(row=3, column=1, pady=5)  # Sil butonunu 3. satır ve 1. sütuna yerleştiriyoruz.

# Mesaj alanı
mesaj = tk.StringVar()  # Kullanıcıya göstermek için bir mesaj değişkeni oluşturuyoruz.
label_mesaj = tk.Label(pencere, textvariable=mesaj)  # Mesaj gösterecek bir etiket oluşturuyoruz.
label_mesaj.grid(row=4, columnspan=2, pady=5)  # Mesaj etiketini 4. satırda yerleştiriyoruz.

# Listbox (rehberdeki kişiler)
listbox = tk.Listbox(pencere, height=10, width=40)  # Rehberdeki kişileri göstermek için bir listbox oluşturuyoruz.
listbox.grid(row=5, columnspan=2, pady=5)  # Listbox'ı 5. satıra ve 2 sütun genişliğine yerleştiriyoruz.

# Pencereyi başlat
pencere.mainloop()  # Tkinter ana döngüsünü başlatıyoruz, böylece pencere etkileşimli hale geliyor.
