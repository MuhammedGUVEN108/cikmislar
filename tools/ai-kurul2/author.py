"""Yerel editoryal AI desteği. Harici model/API çağırmaz; kaynak soruları değiştirmez.
Metinler bu dosyada yazılmıştır; clone eşleştirmeleri açık şık permütasyonlarıdır.
Çalıştırma: py -3 -X utf8 tools/ai-kurul2/author.py
"""
import hashlib, json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[2]
raw = (ROOT/'js/data/archive/questions-kurul-2.js').read_text(encoding='utf-8').strip()
prefix, suffix = 'window.QUESTION_DATA.push(...', ');'
assert raw.startswith(prefix) and raw.endswith(suffix), 'Kaynak veri sarmalayıcısı beklenenden farklı.'
questions = json.loads(raw[len(prefix):-len(suffix)])
Q = {(int(q['year'][:4]), q['number']): q for q in questions}
DATA, OMIT = {}, {}
G = {
 'Genom':'Bir hücrenin taşıdığı genetik materyalin bütünü; yalnız protein kodlayan dizilerden oluşmaz.',
 'Ekzon':'RNA işlenmesinden sonra olgun transkriptte kalan bölüm; her ekzonun tamamı protein kodlamaz.',
 'Karyotip':'Kromozomların sayı ve yapılarının düzenli gösterimi.',
 'PCR':'Belirli bir DNA bölgesinin primerler ve DNA polimerazla döngüler halinde çoğaltılması.',
 'Promotör':'RNA polimeraz ve başlatıcı proteinlerin bir araya gelmesini sağlayan DNA bölgesi.',
 'Transkripsiyon':'DNA kalıbından RNA sentezi; RNA zinciri 5′→3′ yönünde uzar.',
 'Translasyon':'mRNA kodonlarına göre ribozomda polipeptid sentezi.',
 'Nükleozom':'Histon çekirdeği çevresine DNA sarılmasıyla oluşan temel kromatin birimi.',
 'Histon':'DNA paketlenmesine ve kromatin düzenlenmesine katılan protein.',
 'İntron':'Öncü RNA içinde bulunup çoğunlukla kırpılmayla uzaklaştırılan bölüm.',
 'Splicing':'Öncü RNA’dan intronların çıkarılması ve ekzonların birleştirilmesi.',
 'Replikasyon':'DNA’nın yarı korunumlu biçimde kopyalanması.',
 'Ligaz':'Komşu DNA parçaları arasındaki kesintiyi fosfodiester bağı oluşturarak kapatan enzim.',
 'Primer':'Polimerazın uzatabileceği serbest 3′-OH ucu sağlayan kısa nükleik asit.',
 'Telomer':'Doğrusal kromozom uçlarını koruyan tekrarlı DNA ve ilişkili proteinler.',
 'Telomeraz':'Kendi RNA kalıbını kullanarak telomer DNA’sını uzatan ters transkriptaz.',
 'Nükleotid':'Azotlu baz, pentoz şeker ve fosfat içeren birim.',
 'Nükleozit':'Azotlu baz ile pentoz şekerin birleşimi; fosfat içermez.',
 'Fosfodiester bağı':'Nükleik asit omurgasında komşu şekerleri fosfat üzerinden bağlayan kovalent bağ.',
 'tRNA':'Amino asidi 3′ ucunda taşıyan ve antikodonuyla mRNA kodonunu tanıyan adaptör RNA.',
 'Kodon':'mRNA’da bir amino asit veya dur sinyali belirleyen üç nükleotid.',
 'Ribozom':'rRNA ve proteinlerden oluşan, polipeptid sentezinin gerçekleştiği yapı.',
 'Posttranslasyonel modifikasyon':'Protein sentezinden sonra proteinin kesilmesi veya kimyasal olarak değiştirilmesi.',
 'Posttranskripsiyonel modifikasyon':'RNA’nın sentezinden sonra işlenmesi; başlık, poli(A) ve kırpılma gibi süreçler.',
 'Şaperon':'Proteinlerin uygun katlanmasına yardım eden, son yapının parçası olmayan yardımcı protein.',
 'Hipotez':'Veriyle sınanabilir önerme; H₀ genellikle fark veya ilişki bulunmadığını ifade eder.',
 'p değeri':'H₀ ve model varsayımları altında, gözlenen kadar veya daha uç bir sonuç elde etme olasılığı.',
 'Standart hata':'Bir istatistiğin örnekleme dağılımının standart sapması; ortalama için genellikle s/√n ile tahmin edilir.',
 'Standart sapma':'Gözlemlerin ortalamadan ne kadar yayıldığını gösteren ölçü.',
 'Varyans':'Standart sapmanın karesi; yayılım ölçüsü.',
 'Z skoru':'Bir gözlemin ortalamadan kaç standart sapma uzakta olduğunu gösteren (x−μ)/σ değeri.',
 'Tip I hata':'Gerçekte doğru olan H₀’ın reddedilmesi; olasılığı α ile gösterilir.',
 'Tip II hata':'Gerçekte yanlış olan H₀’ın reddedilememesi; olasılığı β ile gösterilir.',
 'Testin gücü':'Gerçekte mevcut bir etkiyi saptama olasılığı; 1−β.',
 'Bağımlı örneklem':'Aynı kişilerin tekrarlı ölçümleri veya eşleştirilmiş gözlemler.',
 'Bağımsız örneklem':'Bir gruptaki gözlemlerin diğer gruptakilerle eşleşmediği örneklem düzeni.',
 'Parametrik test':'Belirli bir dağılım/model ve parametreler üzerinden çıkarım yapan test.',
 'Nonparametrik test':'Sıra veya işaret gibi bilgilere dayanabilen, farklı varsayımları olan test; varsayımsız değildir.',
 'Absorbans':'Işığın örnekten geçerken zayıflamasının logaritmik ölçüsü; A=log₁₀(I₀/I).',
 'Kör':'Analit dışındaki ayıraç ve ortamın ölçüme katkısını düzeltmek için kullanılan örnek.',
 'RCF':'Santrifüjdeki ivmenin yerçekimi ivmesine oranı; rotor yarıçapı ve RPM² ile orantılıdır.',
 'RPM':'Dakikadaki dönüş sayısı; tek başına santrifüj ivmesini belirlemez.',
 'Serum':'Kan pıhtılaştıktan sonra ayrılan sıvı; fibrinojeni tükenmiştir.',
 'Plazma':'Antikoagülanlı kandan ayrılan, fibrinojen içeren sıvı bölüm.',
 'Peptid bağı':'Amino asitlerin karboksil ve amino grupları arasındaki, rezonans nedeniyle kısmi çift bağ karakterli amid bağı.',
 'Primer yapı':'Bir proteinin amino asit dizisi.',
 'Sekonder yapı':'Protein omurgasındaki hidrojen bağlarıyla desteklenen alfa heliks ve beta tabaka gibi yerel düzenler.',
 'Tersiyer yapı':'Tek polipeptid zincirinin üç boyutlu düzeni.',
 'Kuaterner yapı':'Birden fazla polipeptid alt biriminin oluşturduğu protein düzeni.',
 'Disülfid bağı':'İki sisteinin kükürt atomları arasında oluşan kovalent bağ.',
 'Kollajen':'Gly-X-Y tekrarlı, üçlü heliks oluşturan, bağ dokusuna çekme direnci sağlayan protein ailesi.',
 'Elastin':'Lizin türevi çapraz bağlarıyla dokuların esnemesine ve eski biçimine dönmesine yardım eden protein.',
 'Hemoglobin':'Eritrositte oksijen taşıyan, erişkinde başlıca α₂β₂ yapısındaki hem proteini.',
 'Miyoglobin':'Kasta oksijen bağlayan tek zincirli hem proteini; bağlanma eğrisi hiperboliktir.',
 'Kooperativite':'Bir liganda bağlanmanın diğer bağlanma bölgelerinin afinitesini değiştirmesi.',
 '2,3-BPG':'Deoksihemoglobinin T durumunu destekleyip oksijen afinitesini azaltan eritrosit metaboliti.',
 'Amino asit':'Proteinlerde peptid bağlarıyla birleşen, amino ve karboksil grupları taşıyan yapıtaşı.',
 'İzoelektrik nokta':'Bir molekülün ortalama net elektrik yükünün sıfır olduğu pH (pI).',
 'Koenzim':'Enzim tepkimesine katılan organik yardımcı molekül; çoğu vitaminlerle ilişkilidir.',
 'ADP':'Adenozin difosfat; ATP sentezinde fosfat kabul eder.',
 'ATP sentaz':'Protonların elektrokimyasal gradyanını ATP sentezine bağlayan enzim kompleksi.',
 'Fosfolipid':'Fosfatlı polar baş ve hidrofobik bölge taşıyan, zarların temel lipid sınıflarından biri.',
 'Triaçilgliserol':'Gliserole üç yağ asidinin esterleşmesiyle oluşan başlıca yağ depolama molekülü.',
 'Seramid':'Sfingozine amid bağıyla yağ asidi eklenmesiyle oluşan sfingolipid çekirdeği.',
 'Sfingomiyelin':'Seramide fosfokolin eklenmiş, gliserol içermeyen fosfosfingolipid.',
 'DAG':'Diaçilgliserol; PIP₂’nin fosfolipaz C ile kesilmesinde oluşan, zarda kalan ikinci haberci.',
 'IP3':'İnositol 1,4,5-trifosfat; endoplazmik retikulumdan Ca²⁺ salınmasını uyaran ikinci haberci.',
 'PKC':'Protein kinaz C; bazı izoformları DAG ve Ca²⁺ ile etkinleşen protein kinaz ailesi.',
 'cAMP':'ATP’den adenilat siklazla üretilen, PKA’yı etkinleştirebilen ikinci haberci.',
 'AKT':'PI3K yolunda hücre büyümesi ve hayatta kalmasına katılan serin/treonin kinaz; protein kinaz B.',
 'Bazal lamina':'Epitelin altında bulunan, tip IV kollajen ve laminin gibi bileşenler içeren özel matriks tabakası.',
 'Ekstraselüler matriks':'Hücrelerin dışına salgılanan protein ve polisakkaritlerden oluşan destek ve sinyal ortamı.',
 'Western blot':'Proteinlerin ayrılıp membrana aktarılması ve özgül antikorlarla saptanması.',
 'ELISA':'Antijen-antikor bağlanmasını enzimle oluşturulan sinyalle ölçen immünolojik yöntem.',
 'Vitamin':'Normal metabolizma için gereken, vücutta gereksinimi karşılayacak miktarda sentezlenemeyen organik mikrobesin.',
 'Tetrahidrofolat':'Folatın tek karbonlu birim aktarımında görev yapan indirgenmiş koenzim biçimi.',
 'Pantotenik asit':'B5 vitamini; koenzim A ve açil taşıyıcı proteindeki fosfopantetein bileşeninin öncülü.',
 'Tiamin':'B1 vitamini; TPP biçimi transketolaz ve oksidatif dekarboksilasyonlarda görev alır.',
 'Biyotin':'Karboksilazların CO₂ aktarımında kullandığı B7 vitamini.',
 'Kobalamin':'B12 vitamini; metiyonin sentaz ve metilmalonil-KoA mutaz tepkimelerinde görev alır.',
 'Retinal':'Görme pigmentlerinde görev alan A vitamini aldehit formu.',
 'Pekiştirme':'Bir davranışın gelecekte görülme olasılığını artıran sonuç ilişkisi.',
 'Klasik koşullanma':'Başlangıçta nötr olan uyaranın başka bir uyaranla eşleşerek öğrenilmiş tepki oluşturması.',
 'Nükleofil':'Elektron çiftini paylaşarak yeni bağ oluşturan elektronca zengin tür.',
 'Konjuge baz':'Bir asidin proton vermesiyle geride kalan tür.',
 'Aromatiklik':'Düzlemsel ve halkasal, kesintisiz konjuge π sisteminde uygun elektron sayısıyla sağlanan özel kararlılık.',
}
TOPICS={
 'gen':['Genom','Ekzon'], 'chr':['Karyotip','Genom'], 'rna':['Transkripsiyon','Nükleotid'],
 'nuc':['Nükleozom','Histon'],'splice':['Splicing','İntron'],'rep':['Replikasyon','Primer'],
 'tel':['Telomer','Telomeraz'],'translation':['Translasyon','tRNA'],'ptm':['Posttranslasyonel modifikasyon','Posttranskripsiyonel modifikasyon'],
 'stats':['Hipotez','p değeri'],'normal':['Z skoru','Standart sapma'],'se':['Standart hata','Varyans'],
 'paired':['Bağımlı örneklem','Standart hata'],'power':['Testin gücü','Tip II hata'],
 'spectro':['Absorbans','Kör'],'centrifuge':['RCF','RPM'],'serum':['Serum','Plazma'],
 'protein':['Primer yapı','Sekonder yapı'],'peptide':['Peptid bağı','Amino asit'],
 'collagen':['Kollajen','Elastin'],'hb':['Hemoglobin','Miyoglobin'],'aa':['Amino asit','İzoelektrik nokta'],
 'vit':['Vitamin','Koenzim'],'energy':['ADP','ATP sentaz'],'lipid':['Fosfolipid','Triaçilgliserol'],
 'sphingo':['Seramid','Sfingomiyelin'],'signal':['DAG','IP3'],'akt':['AKT','PKC'],
 'ecm':['Ekstraselüler matriks','Bazal lamina'],'lab':['PCR','Western blot'],
 'psych':['Pekiştirme','Klasik koşullanma'],'chem':['Nükleofil','Konjuge baz'],
}
G.update({
 'Karbonhidrat':'Monosakkaritleri ve bunların polimer/türevlerini içeren molekül sınıfı; enerji ve yapısal işlevleri vardır.',
 'Glikozidik bağ':'Bir şekerin anomerik karbonunun başka bir gruba bağlandığı kovalent bağlantı.',
 'Km':'Basit Michaelis–Menten modelinde tepkime hızının Vmax/2 olduğu substrat derişimi.',
 'Vmax':'Verilen aktif enzim miktarında substrat doygunluğuna yaklaşırken erişilen en yüksek tepkime hızı.',
 'Enzim':'Tepkimenin aktivasyon enerjisini düşürerek hızı artıran biyolojik katalizör; denge sabitini değiştirmez.',
 'Fonksiyonel grup':'Organik molekülün karakteristik tepkimelerine katılan atom veya atom grubu.',
 'Hidrojen bağı':'Hidrojenin elektronegatif atoma bağlı olduğu uygun gruplar arasında oluşabilen yönlü etkileşim.',
 'İzomer':'Aynı molekül formülünü taşıyıp atom bağlantısı veya uzaysal düzeni farklı olan bileşik.',
 'Karbonil':'Karbon ve oksijen arasında çift bağ içeren C=O grubu.',
 'Alken':'Karbon-karbon çift bağı taşıyan hidrokarbon sınıfı.',
 'Oksidasyon':'Elektron kaybı veya organik kimyada sıklıkla oksijene bağ artışı/hidrojen kaybıyla ilişkili dönüşüm.',
 'İndirgenme':'Elektron kazanımı veya organik kimyada sıklıkla hidrojene bağ artışı/oksijene bağ azalmasıyla ilişkili dönüşüm.',
 'Bilişsel gelişim':'Algılama, düşünme, bellek ve problem çözme yetilerindeki gelişimsel değişim.',
 'Piaget evreleri':'Duyu-motor, işlem öncesi, somut işlemler ve soyut/formel işlemler olarak tanımlanan bilişsel gelişim evreleri.',
 'Agorafobi':'Kaçmanın veya yardım almanın zor olacağı düşünülen durumlara ilişkin belirgin korku ve kaçınma.',
 'Kaygı':'Olası tehdit veya olumsuz sonuca yönelik beklentiyle ilişkili duygusal ve bedensel yanıt.',
 'Psikososyal gelişim':'Erikson yaklaşımında bireyin yaşam boyunca toplumsal ilişkiler içinde çözmeye çalıştığı gelişimsel çatışmalar.',
 'Girişimcilik':'Erikson’un okul öncesi evresinde yeni etkinlik başlatma ve çevreyi keşfetme yönelimi.',
 'Popülasyon':'Araştırma sonucunun genellenmek istendiği tüm birimler.',
 'Örneklem':'Popülasyonun araştırmada gözlenen alt kümesi.',
 'DNA onarımı':'DNA lezyonlarını tanıyan ve uygun baz/omurga yapısını geri kazandırmaya çalışan hücresel yollar.',
 'Yanlış eşleşme onarımı':'Replikasyon sonrası hatalı baz eşleşmelerini ve kısa ekleme-silme ilmeklerini düzelten sistem.',
 'Egzositoz':'Vezikülün hücre zarıyla kaynaşarak içeriğini dışarı salması.',
 'SNARE':'Vezikül ile hedef zarın kaynaşmasına yardım eden protein ailesi.',
})
TOPICS.update({'carb':['Karbonhidrat','Glikozidik bağ'],'enzyme':['Km','Vmax'],'coenzyme':['Koenzim','Nükleotid'],
 'organic':['Fonksiyonel grup','Karbonil'],'boiling':['Hidrojen bağı','Fonksiyonel grup'],
 'isomer':['İzomer','Fonksiyonel grup'],'oxidation':['Oksidasyon','İndirgenme'],
 'development':['Bilişsel gelişim','Piaget evreleri'],'agora':['Agorafobi','Kaygı'],
 'erikson':['Psikososyal gelişim','Girişimcilik'],'population':['Popülasyon','Örneklem'],
 'repair':['DNA onarımı','Yanlış eşleşme onarımı'],'neurotoxin':['Egzositoz','SNARE']})
def add(y,n,topic,summary,reasons):
    key=(y,n);q=Q[key]; rr=reasons.split(' | ')
    assert len(rr)==5,(key,len(rr));assert key not in DATA and key not in OMIT,key
    terms=list(TOPICS[topic]); hay=(summary+' '+q['stem']+' '+' '.join(o['text'] for o in q['options'])).casefold()
    for term in G:
        if term not in terms and term.casefold() in hay and len(terms)<6:terms.append(term)
    DATA[key]={'summary':summary,'options':[{'label':o['label'],'optionText':o['text'],'reason':r,'isCorrect':o['label'] in q['sourceKeys']} for o,r in zip(q['options'],rr)],'terms':terms,'topic':topic,'provenance':'ai_authored','academicVerification':False}
def clone(y,n,sy,sn,order='ABCDE',summary=None):
    base=DATA[sy,sn]; rr=[base['options'][ord(c)-65]['reason'] for c in order]
    assert {Q[y,n]['options'][i]['label'] for i,c in enumerate(order) if base['options'][ord(c)-65]['isCorrect']}==set(Q[y,n]['sourceKeys']),('Anahtar/şık eşleştirmesi',y,n,sy,sn,order)
    add(y,n,base['topic'],summary or base['summary'],' | '.join(rr))
def omit(y,n,reason):
    assert (y,n) not in DATA and (y,n) not in OMIT,(y,n)
    OMIT[y,n]=reason
def retag(y,n,topic):
    if (y,n) not in DATA:return
    old=DATA.pop((y,n))
    add(y,n,topic,old['summary'],' | '.join(o['reason'] for o in old['options']))

# 2021–2022. Yalnız tam ve tek anlamlı kaynak sorular.
add(2021,1,'gen','Protein kodlayan diziler insan genomunun yaklaşık %1,5’idir. İntronları ve düzenleyici alanları içeren gen bölgeleriyle yalnız kodlayan dizileri ayırmak gerekir.','Yaklaşık %1,5, protein kodlayan diziler için uygun büyüklüktür. | %30 yalnız protein kodlayan bölüm için çok yüksektir; daha geniş gen bölgeleriyle karıştırılmamalıdır. | %20 kodlayan dizilerin payını belirgin biçimde aşar. | %8 protein kodlayan diziler için beklenen pay değildir. | Genomun yarısı protein kodlamaz; kodlamayan diziler çoğunluktadır.')
add(2021,3,'chr','Karyotipleme, kromozomların sayı ve büyük ölçekli yapı değişikliklerini incelemek için kullanılır. Baz dizisini okumakla aynı analiz değildir.','Sanger analizi nükleotid dizisini okur; tüm kromozomları karyotip halinde göstermez. | Karyotipleme kromozomları görüntüleyip sayı ve yapı yönünden karşılaştırır. | Gerçek zamanlı PCR seçilmiş DNA hedeflerini çoğaltır ve sinyali izler. | Hemogram kan hücrelerini sayar ve hücresel parametreleri ölçer. | Hemoglobin elektroforezi hemoglobin türlerini ayırır; kromozom analizi değildir.')
add(2021,7,'gen','Promotör, ekzon, intron ve UTR gen bölgesinde tanımlanan yapılardır. Sentromer ise kromozom düzeyinde, ayrılma ve kinetokor oluşumuyla ilişkili özel bölgedir.','Promotör genin transkripsiyon başlangıcını düzenleyen bölgesidir. | 3′ UTR transkriptte kalır fakat proteine çevrilmez. | Ekzon olgun transkriptte kalan gen bölümüdür. | İntron öncü RNA’dan kırpılan gen bölümüdür. | Sentromer genin standart yapısal parçası değil, kromozomun ayrılma bölgesidir.')
add(2021,9,'nuc','Nükleozom çekirdeği H2A, H2B, H3 ve H4’ten ikişer kopya içeren histon oktameridir. Yaklaşık 147 baz çifti DNA bunun çevresine yaklaşık 1,7 tur sarılır.','Kromozom uçları telomer olarak adlandırılır. | Kinetokorun kurulduğu bölge sentromerdir; nükleozom değildir. | Histon oktameri çevresine DNA sarılması nükleozomun temel yapısını tanımlar; “iki tur” yaklaşık anlatımdır. | İnterfazdaki DNA-protein örgütünün genel adı kromatindir. | Eski viral DNA kalıntıları genomdaki tekrarlı elemanlardır; nükleozomun tanımı değildir.')
add(2021,11,'rna','DNA’dan RNA sentezine transkripsiyon denir. Translasyon ise mRNA bilgisinin polipeptide çevrilmesidir.','Translasyon RNA’dan protein sentezidir. | Replikasyon DNA’nın kopyalanmasıdır. | Transkripsiyon DNA kalıbından RNA sentezidir. | Ekspresyon gen bilgisinin işlevsel ürüne dönüşmesinin genel adıdır. | Transpozisyon hareketli genetik elemanların yer değiştirmesidir.')
add(2021,12,'splice','Splicing sırasında öncü mRNA’daki intronlar çıkarılır ve ekzonlar birleştirilir. Bu işlem RNA olgunlaşmasıdır; protein sentezi veya DNA eşlenmesi değildir.','tRNA’nın ribozoma bağlanması translasyonda gerçekleşir. | mRNA’nın küçük ribozom alt birimine bağlanması translasyon başlangıcıdır. | İntronların öncü mRNA’dan uzaklaştırılması splicing işlemidir. | Polipeptid uzaması translasyonun elongasyon aşamasıdır. | DNA kopyalanması replikasyondur; RNA kırpılması değildir.')
add(2021,13,'stats','Hipotezin yönü alternatif hipotezde belirtilir: büyük/küçük yönlü ya da yalnız farklılık belirten çift yönlü olabilir. H₀ genellikle farkın bulunmadığı durumu ifade eder.','Araştırma hipotezi çalışmanın sınadığı soruyu somutlaştırır. | Hipotez verilerle test edilen bir öngörüdür. | Alternatif hipotez H₀’ın eşitlik/farksızlık savının karşısındadır. | Yönü sıfır hipotezi belirlemez; yönlü alternatif hipotez belirler. | Alternatif hipotez tek veya çift yönlü kurulabilir.')
add(2021,14,'normal','Z=(20−22)/10=−0,2. Alt kuyruk alanı 0,5−0,0793=0,4207’dir. 1000×0,4207≈421 kişi; seçeneklerde yaklaşık karşılığı 420’dir.','508 kişi, alt kuyruk için gereken yaklaşık %42 oranını sağlamaz. | 579 yaklaşık üst kuyruk oranıdır; sorulan 20’nin altıdır. | 301, 0,2 yerine farklı Z alanı kullanılmasıyla oluşabilecek hatalı sonuçtur. | 1000×0,4207≈421; yaklaşık 420 seçeneği uygundur. | 492, Z=−0,02 alanının yanlış kullanılmasına yakındır; doğru Z=−0,2’dir.')
add(2021,16,'paired','Eşleştirilmiş t testi sürekli bir değişkenin aynı kişideki iki ölçümü gibi bağımlı verilerde kullanılır. Normal dağılım varsayımı iki grubun ayrı ayrı değerleri için değil farklar içindir.','I doğrudur ancak farkların yaklaşık normal dağılması şartını tek başına kapsamaz. | II yanlıştır; bu test bağımsız değil eşleştirilmiş ölçümler içindir. | III doğrudur ancak sürekli değişken koşulu da gereklidir. | Bağımsız grup koşulu nedeniyle II’yi içeren bu birleşim uygun değildir. | I ve III birlikte uygundur; eşleştirilmiş farklar üzerinden t testi yapılır.')
add(2021,20,'stats','Küme örnekleme olasılıklı tasarımla kümelerin seçilmesidir. Kota ve kartopu tipik olasılıksız örnekleme yöntemleridir.','Kota örneklemesinde bilinen seçilme olasılıkları zorunlu değildir; eşleşme uygundur. | Basit rastgele seçim olasılıklı örneklemedir. | Rastgele küme seçimi olasılıklıdır; “olasılıklı olmayan” eşleştirmesi yanlıştır. | Kartopu örnekleme katılımcı yönlendirmesine dayanır ve tipik olarak olasılıksızdır. | Rastgele başlangıçlı sistematik örnekleme olasılıklı tasarımdır.')
add(2021,23,'stats','Test türü değişkenin ölçeği, dağılımı, örneklem büyüklüğü ve bağımlılık düzenine göre seçilir. α karar eşiğidir; bu bağlamda hangi test ailesinin seçileceğini belirleyen veri özelliği değildir.','Dağılım ve varsayımlar test seçimini etkiler. | Yanılma düzeyi karar eşiğini belirler; değişkenin yapısına uygun test ailesini seçen özellik değildir. | Sayısal, kategorik veya sıralı değişken farklı analiz gerektirir. | Örneklem büyüklüğü yaklaşımın geçerliliğini ve kesin test gereksinimini etkiler. | Eşleştirilmiş ve bağımsız gözlemler farklı testler gerektirir.')
add(2021,25,'energy','ADP arttığında ATP sentazın kullanabileceği substrat artar; proton gradyanının kullanılması elektron taşınmasını hızlandırır. Enerji talebine bağlı bu düzenleme solunumsal kontroldür.','NADH elektron vericisidir; sorudaki enerji talebini bildiren temel kontrol molekülü değildir. | NAD⁺ yükseltgenmiş elektron taşıyıcısıdır. | FAD redoks kofaktörüdür; ATP sentezinin fosfat kabul edeni değildir. | ADP ATP sentezinin substratı olarak solunum hızını enerji tüketimine bağlar. | FADH₂ elektron sağlar; sorudaki başlıca talep düzenleyicisi ADP’dir.')
add(2021,27,'collagen','Desmozin elastinin lizin türevi çapraz bağıdır. Kollajende hidroksilasyon, glikozilasyon ve üçlü heliks bulunur; elastin esnek ağ yapar.','Gly-X-Y kollajen için karakteristiktir; elastinde aynı düzenli tekrar bulunmaz. | Kollajen glikozillenebilir; elastin klasik olarak glikozillenmiş kollajen yapısından ayrılır. | Hidroksilizin kollajen için belirgindir; elastinin çapraz bağları başlıca lizinden türetilir. | Desmozin kollajene değil elastine aittir; çapraz bağ türleri ters verilmiştir. | Kollajen düzenli üçlü heliks, elastin esnek düzensiz ağ oluşturur.')
add(2021,29,'ecm','Tenasin, hücre-matriks etkileşimlerini düzenleyen matriks glikoproteinidir. Kollajen ve elastin gibi temel lif proteinlerinden farklı işlevsel/adezyon düzenleyici sınıfta değerlendirilir.','Kollajen çekme direnci sağlayan temel yapısal proteindir. | Retiküler lifler başlıca tip III kollajen içerir ve yapısal destek sağlar. | Elastin dokuya esneklik sağlayan yapısal proteindir. | Proteoglikanlar su tutan matriks ağının temel bileşenidir. | Tenasin hücre adezyonu ve matriks etkileşimlerini düzenleyen glikoproteindir.')
add(2021,30,'spectro','Tungsten lamba görünür ve yakın kızılötesi bölge için yaygın kaynaktır. Döteryum ve hidrojen lambaları özellikle UV bölgesiyle ilişkilidir.','Döteryum UV ölçümlerinde kullanılan sürekli ışık kaynağıdır. | Tungsten görünür ve yakın IR bölge için uygundur. | Ksenon geniş spektrum sunabilir; sorudaki klasik 320–3000 nm eşleşmesi tungsten lambadır. | Cıva lambası belirgin çizgisel emisyonlarıyla bilinir. | Hidrojen özellikle UV kaynağı olarak değerlendirilir.')
add(2021,32,'spectro','Beer–Lambert bağıntısı A=εlc’dir. Sabit koşullarda derişim veya yol uzunluğu arttıkça absorbans artar; geçen ışığın oranı azalır. Standart bilinen analit derişimi, kör ise arka plan düzeltmesi sağlar.','II doğrudur ama I, III ve IV de doğrudur. | III ve IV, absorbansın derişim ve yol uzunluğuyla ilişkisini doğru verir. | Kör optik arka planı düzeltmek için kullanılır; II yanlış değildir. | Standart bilinen derişimdir; I yanlış değildir. | Dört önerme de standart fotometrik ölçüm çerçevesiyle uyumludur.')
add(2021,33,'ptm','5′ cap, mRNA’ya eklenen RNA işleme modifikasyonudur. Protein üzerindeki glikozilasyon, disülfid, metilasyon ve proteolitik kesilme ise protein olgunlaşması kapsamındadır.','Proteine şeker eklenmesi glikozilasyondur ve protein modifikasyonudur. | Sisteinler arası disülfid oluşumu protein katlanmasını kararlılaştırabilir. | Protein kalıntıları metillenebilir; bu protein modifikasyonudur. | Proteolitik kesilme protein olgunlaşmasına örnektir. | 5′ cap proteine değil RNA’ya eklenir; posttranskripsiyoneldir.')
add(2021,34,'translation','Bakteriyel EF-Tu, GTP’ye bağlı halde aminoaçil-tRNA’yı ribozomun A bölgesine getirir. IF başlangıç, RF sonlandırma faktörleridir.','IF-2 başlangıçta başlatıcı tRNA’nın yerleşmesine yardım eder. | EF-Tu uzamada aminoaçil-tRNA taşır. | IF3 başlangıç kompleksinin doğru kurulmasına katılır. | RF1 dur kodonunu tanıyan sonlandırma faktörüdür. | RF3 sonlandırmaya yardımcı GTPazdır; elongasyon faktörü değildir.')
add(2021,35,'translation','Bakterilerin 70S ribozomu 30S ve 50S alt birimlerden oluşur. Başlatıcı tRNA formilmetiyonin taşır; mRNA ile birlikte başlangıç kompleksi kurulur.','70S, başlatıcı fMet-tRNA ve mRNA bakteriyel başlangıç kompleksine uygundur. | Bakterilerin tipik başlatıcı amino asidi formillenmiş metiyonindir. | 80S sitozolik ökaryot ribozomudur; prokaryot başlangıcına uymaz. | fMet bakteriyel olsa da 80S ribozom eşleştirmesi yanlıştır. | 40S ökaryotik küçük alt birimdir ve tamamlanmış prokaryotik ribozom değildir.')
add(2021,36,'ptm','RNA’ya CCA, cap ve poli(A) eklenmesi ile intron çıkarılması RNA işleme basamaklarıdır. N-terminal sinyal peptidinin kesilmesi proteine uygulanan işlemdir.','CCA tRNA’nın amino asit bağlayan 3′ ucunu oluşturur. | Cap ökaryotik mRNA’nın 5′ ucuna eklenir. | Poli(A) kuyruğu çoğu ökaryotik mRNA’nın 3′ ucuna eklenir. | Sinyal peptidi amino asitlerden oluşur; kesilmesi RNA değil protein işlenmesidir. | İntronların çıkarılması RNA splicing işlemidir.')
add(2021,37,'rna','RNA DNA kalıbına tamamlayıcı ve antiparaleldir. 5′-TAACGG-3′ kalıbının karşılığı 3′-AUUGCC-5′ olur; RNA’yı 5′→3′ yazınca 5′-CCGUUA-3′ elde edilir.','Bu dizi kalıba doğru antiparalel tamamlayıcılığı sağlamaz. | Tamamlayıcılık ve yön birlikte korunduğunda 5′-CCGUUA-3′ bulunur. | RNA’da timin yerine urasil bulunmalıdır; ayrıca dizi tamamlayıcı değildir. | Tamamlayıcı bazlar bu sırayla 3′→5′ yönünde olur; uçlar yanlış verilmiştir. | RNA’da T kullanılmıştır ve doğru ters tamamlayıcı dizilim değildir.')
add(2021,38,'energy','Ubikinon, lipid çözünür bir kinon ve izoprenoid zincir taşır; nükleotid yapısı içermez. NADP, FAD, SAM ve PAPS ise adenozin içeren yapılardır.','NADP nikotinamid ve adenine bağlı nükleotid yapıları içerir. | FAD, flavin adenin dinükleotiddir. | SAM, S-adenozilmetiyonindir; adenozin içerir. | PAPS, fosfoadenozin fosfosülfattır; adenozin içerir. | Koenzim Q kinon yapılıdır; nükleozit veya nükleotid içermez.')
add(2021,39,'rna','Baz ile pentoz arasında N-glikozidik bağ kurulur. Fosfodiester bağı ise nükleik asit omurgasında komşu nükleotidleri bağlar.','Hidrojen bağları karşılıklı baz eşleşmesinde görev yapar. | Fosfodiester bağı şeker-fosfat omurgasındaki nükleotidler arasındadır. | Pürin N9 atomu ile şekerin C1′ atomu arasında N-glikozidik bağ vardır. | Van der Waals etkileşimleri baz-şeker arasındaki kovalent bağın adı değildir. | Peptid bağı amino asitleri bağlar; baz-şeker bağlantısı değildir.')
add(2021,40,'lipid','Dihidroksiaseton ketotrioz; sorbitol şeker alkolü; glukozamin aminoşeker; glukuronat şeker asididir. Eşleştirme sırası 6-3-1-2 olur.','Sorbitol ketotrioz değildir; ilk eşleştirmeden yanlıştır. | Gliseraldehit aldotriozdur, ketotrioz değildir. | Gliseraldehitin ketotrioz, ksilülozun şeker alkolü sayılması yanlıştır. | 6-3-1-2 sırası dört sınıfı da doğru eşleştirir. | Ksilüloz ketopentozdur; şeker alkolü sorbitol olmalıdır.')
add(2021,42,'spectro','A=εlc bağıntısında derişim arttıkça absorbans artar. UV ölçümünde UV’yi geçiren kuvars küvet kullanılır.','Standart çözeltinin derişimi bilinmektedir. | Kör analit dışı optik katkıyı düzeltir. | Sabit derişimde absorbans optik yol uzunluğuyla orantılıdır. | Kuvars UV ışığını geçirdiği için UV ölçümlerine uygundur. | Derişim artınca absorbans azalmaz; doğrusal çalışma aralığında artar.')
add(2021,43,'spectro','Köre göre düzeltilmiş aynı koşullardaki absorbanslar derişimle orantılıdır. C=10×(0,500/0,250)=20 g/dL.','Absorbans iki katına çıktığından derişim 20 g/dL olur. | Aynı derişim ancak eşit absorbanslarla beklenirdi. | 5 g/dL, oranı ters kullanma hatasıdır. | 15 g/dL absorbansların 2 oranını karşılamaz. | 40 g/dL için standarttan dört kat absorbans beklenirdi.')
add(2021,45,'collagen','Kollajen hidroksilizin kalıntılarına bağlı şekerler içerebilir. Üçlü heliks ve her üç kalıntıda bir glisin kollajenin ayırt edici özellikleridir.','Elastin kollajendeki gibi düzenli üçlü heliks oluşturmaz. | Kollajenin tipik tekrarı Gly-X-Y’dir. | Hidroksilizin kollajenin karakteristik modifiye amino asitlerindendir. | Kollajen glikozillenebilir; karbonhidrat içermez ifadesi yanlıştır. | Elastindeki desmozin çapraz bağları lizin türevlerinden oluşur.')
add(2021,46,'peptide','Peptid bağı rezonans nedeniyle düzlemsel ve kısmi çift bağ karakterlidir. Çoğunlukla trans düzenlenir; özellikle prolin içeren bağlarda cis oranı artabilir.','Peptid bağı karboksil ve amino grupları arasında oluşan amid bağıdır. | Amino asitleri birleştiren bağ kovalenttir. | Rezonans C–N bağının serbest dönüşünü kısıtlar. | Genel düzen cis değil trans olduğundan bu ifade yanlıştır. | Peptid grubu polar olsa da fizyolojik pH’da genellikle net yüksüzdür.')
add(2021,47,'protein','Sekonder yapının temel kararlılığı omurgadaki C=O ve N–H gruplarının hidrojen bağlarından gelir. Hidrofobik etki esas olarak üç boyutlu katlanmada önemlidir.','Prolin dönüşe uygun geometri, glisin esneklik sağlar. | Alfa helikste yan zincirler dışarıya yönelir. | Hidrofobik etki ve uygun proteinlerde disülfid bağları tersiyer yapıyı destekler. | Peptid bağlarının hidrolizi amino asit dizisini, dolayısıyla primer yapıyı bozar. | Sekonder yapının temel bağları hidrojen bağlarıdır; hidrofobik etkiyle karıştırılmıştır.')
add(2021,48,'lipid','Daha yüksek sıcaklık, daha kısa zincirler ve cis doymamışlık genellikle zar akışkanlığını artırır. Kolesterol sıcaklığa bağlı olarak akışkanlığı tamponlar.','Kısa zincirler daha zayıf paketlendiğinden akışkanlığı artırır. | Cis çift bağlar sık paketlenmeyi bozarak akışkanlığı artırır. | Sıcaklık artışı genel olarak akışkanlığı artırır; ters orantı ifadesi yanlıştır. | Kolesterol düşük sıcaklıkta sıkı paketlenmeyi, yüksek sıcaklıkta aşırı hareketi sınırlar. | Cis kıvrımı zincirlerin düzenli paketlenmesini zorlaştırır.')
add(2021,49,'hb','Hemoglobinin oksijen eğrisi alt birimler arası kooperativite nedeniyle sigmoidaldir. Miyoglobinin tek bağlanma bölgesi olduğundan eğrisi hiperboliktir.','Distal E7 histidin oksijen bağlanma çevresini düzenler. | Hemoglobin proton bağlayarak tamponlamaya katılır. | Proksimal F8 histidin hem demirini globin zincirine bağlar. | Hemoglobinin eğrisi hiperbolik değil sigmoidaldir. | Miyoglobin düşük oksijen basınçlarında oksijeni daha sıkı bağlar.')
add(2021,50,'hb','Miyoglobin tek zincirlidir ve oksijeni kooperativite göstermeden bağlar; eğrisi hiperboliktir. Oksijen bağlayan hem demiri Fe²⁺ halinde olmalıdır.','Miyoglobinin eğrisi sigmoid değil hiperboliktir. | Hem demirinin dört koordinasyonu porfirindeki azotlarla kurulur. | Proksimal histidinin imidazol azotu demire bağlanır. | Fe³⁺ içeren methemoglobin oksijeni normal hemoglobin gibi bağlayamaz. | Miyoglobin kasta oksijen deposu ve hücre içi taşınmasına katkı sağlar.')
add(2021,51,'hb','2,3-BPG deoksihemoglobinin T durumuna bağlanarak oksijen afinitesini azaltır. Bu, eğriyi sağa kaydırıp dokuda oksijen bırakılmasını kolaylaştırır.','2,3-BPG eritrosit glikolizinin Rapoport–Luebering yan yolunda oluşur. | T durumunun kararlılığını artırır. | Azalan afinite oksijen eğrisinin sağa kaymasına yol açar. | 2,3-BPG afinitesini artırmaz; azaltır. | Yüksek irtifaya uyumda eritrosit 2,3-BPG düzeyi artabilir.')
add(2021,53,'aa','Fizyolojik pH’da aspartat ve glutamatın yan zincir karboksilleri çoğunlukla deprotonlanmış, negatif yüklüdür. Lizin ve arginin bazik, alanin yüksüz yan zincirlidir.','Alanin yüksüz, lizin pozitif yan zincirlidir. | Alanin yüksüz; lizin ve arginin pozitif yan zincirlidir. | Aspartat negatif olsa da alanin ve arginin bu gruba uymaz. | Lizin ve arginin fizyolojik pH’da pozitif yan zincirlidir. | Glutamat ve aspartat asidik, negatif yüklü yan zincir taşır.')
add(2021,55,'vit','Tetrahidrofolat farklı yükseltgenme düzeylerindeki tek karbonlu birimleri taşır. Biyotinle taşınan CO₂ aynı tek-karbon havuzuyla karıştırılmamalıdır.','Biyotin karboksilazlarda CO₂ taşır. | B6’nın aktif formu amino asit metabolizmasında görev alır. | Tetrahidrofolat tek karbonlu birim aktarımının temel koenzimidir. | Askorbat indirgen ve hidroksilasyon tepkimelerine yardımcıdır. | Riboflavin FAD ve FMN’nin öncülüdür.')
add(2021,56,'translation','Botulinum toksini SNARE proteinlerini keserek sinaptik vezikülün zarla kaynaşmasını engeller. Böylece asetilkolin egzositozu azalır.','Temel hedef DNA’dan RNA sentezi değildir. | Temel hedef RNA’nın başlık veya kırpılma işlemi değildir. | Temel mekanizma ribozomal protein sentezinin genel durdurulması değildir. | SNARE kesilmesi vezikül füzyonunu ve nörotransmitter egzositozunu engeller. | Genel protein modifikasyonu yerine belirli SNARE proteinlerinin proteolitik kesilmesiyle salıverme engellenir.')
add(2021,57,'centrifuge','RCF, santrifüjde örneğe etki eden ivmeyi yerçekimine göre ifade eder. Aynı RPM farklı rotor yarıçaplarında farklı RCF oluşturabilir.','Tüp boyu tek başına örneğin maruz kaldığı ivmeyi belirlemez. | RPM yalnız dönüş hızıdır; rotor yarıçapı bilinmeden RCF hesaplanamaz. | RCF örneğin maruz kaldığı bağıl santrifüj ivmesini doğrudan belirtir. | Sabit açılı rotor geometrisi tek başına kuvvet değerini vermez. | Sıcaklık örnek korunmasını etkiler fakat santrifüj ivmesinin ölçüsü değildir.')
add(2021,58,'lipid','Trombosit aktive edici faktörde gliserolün birinci karbonundaki zincir eter bağıyla bağlanır. Bu yapı onu tipik ester bağlı gliserofosfolipidlerden ayırır.','Lesitin fosfatidilkolindir; klasik formunda yağ asitleri esterle bağlıdır. | PAF, sn-1’de eter bağlı alkil zincir taşıyan gliserofosfolipiddir. | Sefalin adı fosfatidiletanolamin gibi klasik gliserofosfolipidlerle ilişkilidir. | Fosfatidilgliserol tipik olarak ester bağlı açil zincirleri taşır. | Kardiyolipin iki fosfatidatın gliserolle bağlandığı difosfatidilgliseroldür.')
add(2021,59,'signal','PIP₂ fosfolipaz C tarafından kesilince DAG ve IP₃ oluşur. DAG zarda kalır, IP₃ hücre içinde Ca²⁺ salınmasını uyarır.','PIP₂, DAG ve IP₃ ikinci habercilerinin öncüsüdür. | Fosfatidilserin membran asimetrisi ve apoptoz işaretlenmesinde önemlidir; bu yolun DAG/IP₃ öncüsü değildir. | Fosfatidilkolin önemli zar bileşenidir; klasik PIP₂ yolunun substratı değildir. | Fosfatidiletanolamin yapısal zar fosfolipididir. | Plazmalojen eter lipididir; klasik IP₃ üretiminin substratı değildir.')
add(2021,60,'lipid','Sitozolik gliserol-3-fosfat dehidrogenaz DHAP’ın karbonil grubunu NADH kullanarak indirger. Ürün, gliserolipid sentezinde kullanılan gliserol-3-fosfattır.','Propionat bu indirgenme tepkimesinin substratı değildir. | Laktat bu enzimle gliserol-3-fosfata dönüşmez. | Piruvat laktat dehidrogenazla indirgenebilir; sorudaki tepkime farklıdır. | Gliseraldehit-3-fosfat aldoz fosfattır; hedef substrat DHAP’tır. | DHAP’ın indirgenmesi gliserol-3-fosfat oluşturur.')
add(2021,61,'lipid','Mumlar uzun zincirli yağ asitleriyle uzun zincirli tek hidroksilli alkollerin esterleridir. Triaçilgliserollerdeki üç karbonlu gliserolden ayrılırlar.','Prostaglandinler eikozanoid sinyal molekülleridir. | Uzun zincirli yağ asidi–uzun zincirli alkol esteri mumdur. | Steroller kaynaşmış halkalı steroid alkol yapısındadır. | Sülfolipidler kükürt içeren polar başlı lipidlere verilen addır. | Fosfolipidler fosfatlı polar baş içerir; verilen basit ester tanımı mumdur.')
add(2021,64,'vit','Pantotenik asit, koenzim A ve açil taşıyıcı proteinin fosfopantetein kolunun bileşenidir. Bu kol açil gruplarını taşır.','Folat tek karbon aktarımında görev yapar. | Niasin NAD ve NADP’nin öncülüdür. | Pantotenat CoA ve ACP’nin fosfopantetein bölümüne katılır. | B6 amino asit metabolizmasının PLP koenzimini oluşturur. | Riboflavin FAD ve FMN’ye katılır.')
add(2021,65,'vit','Çiğ yumurta akındaki avidin biyotini bağlayarak emilimini azaltabilir. Isıtma avidinin yapısını bozarak bağlama etkisini azaltır.','Avidinin başlıca bağladığı vitamin tiamin değildir. | Riboflavin FAD/FMN öncülüdür; avidinin hedefi değildir. | Niasin NAD/NADP öncülüdür; avidine özgü değildir. | Avidin biyotine güçlü bağlanır ve emilimini azaltır. | Folat avidinin özgül hedefi değildir.')
add(2021,66,'vit','D vitamini eksikliği kemik mineralizasyonunu bozar. Büyüme plakları açık çocuklarda raşitizm, erişkinde osteomalazi ortaya çıkabilir.','Riboflavin eksikliği bu klasik mineralizasyon bozukluğunun nedeni değildir. | C vitamini eksikliği kollajen bozukluğu ve skorbüt yapar. | D vitamini kalsiyum-fosfat dengesini ve mineralizasyonu destekler. | A vitamini başlıca görme ve epitel farklılaşmasıyla ilişkilidir. | Biyotin karboksilaz koenzimidir; sorudaki hastalık eşleşmesi değildir.')
add(2021,67,'vit','K vitamini, pıhtılaşma proteinlerindeki glutamatın γ-karboksilasyonuna yardım eder. Oluşan Gla kalıntıları Ca²⁺ bağlanmasını sağlar.','A vitamini görme ve gen düzenlenmesinde işlev görür. | D vitamini kalsiyum-fosfat metabolizmasını düzenler; γ-karboksilaz kofaktörü değildir. | E vitamini lipid fazında antioksidandır. | K vitamini glutamatın γ-karboksilasyonu için gereklidir. | B12 metiyonin sentaz ve metilmalonil-KoA mutazla ilişkilidir.')
add(2021,68,'vit','D vitamini karaciğerde 25-hidroksillenip böbrekte 1α-hidroksillenerek aktif kalsitriol biçimine ulaşır. Sorudaki iki organlı aktivasyon bu vitamini tanımlar.','A vitamininin metabolizması bu ardışık karaciğer-böbrek aktivasyonuyla tanımlanmaz. | C vitamini için bu tür iki aşamalı hormon aktivasyonu gerekmez. | D vitamini karaciğer ve böbrekte ardışık hidroksilasyonla aktifleşir. | E vitamini bu aktivasyon yolunu kullanmaz. | K vitamini döngüsüyle yeniden indirgenir; verilen karaciğer-böbrek dizisi D vitaminine aittir.')
add(2021,72,'sphingo','Sfingomiyelin sfingozin omurgası taşıdığı halde fosfokolin baş grubu nedeniyle fosfolipid olarak da sınıflandırılır. Diğer seçenekler seramid veya glikosfingolipid türevleridir.','Seramid sfingolipid çekirdeğidir; kendi başına fosfatlı baş grup taşımaz. | Sfingomiyelin hem sfingolipid hem fosfolipiddir. | Serebrozid tek şekerli glikosfingolipiddir. | Sülfatid sülfatlanmış glikosfingolipiddir; fosfat grubu ile tanımlanmaz. | Globozid nötr oligosakkaritli glikosfingolipiddir.')
add(2021,73,'lipid','Kardiyolipin mitokondri iç zarında bulunan difosfatidilgliseroldür. Kardiyolipin içeren antijen karışımları sifilizde nontreponemal testlerde kullanılır; bunlar tek başına treponemaya özgü testler değildir.','Lesitin fosfatidilkolindir; soruda hedeflenen lipid değildir. | Sefalin fosfatidiletanolamin gibi fosfolipidler için kullanılan addır. | Kardiyolipin klasik nontreponemal test antijen karışımının bileşenidir. | Fosfatidilserin bu klasik kalp kası antijeni eşleşmesi değildir. | Fosfatidiletanolamin temel zar lipididir; hedef kardiyolipindir.')
add(2021,74,'rep','Tek iplik bağlayan proteinler ayrılmış DNA ipliklerini kararlı tutup yeniden eşleşme ve ikincil yapı oluşumunu önler. Helikazın görevi ise çift sarmalı açmaktır.','SSB proteinleri açık ipliği kaplayarak katlanma ve yeniden eşleşmeyi önler. | Helikaz çift sarmalı açar; açık ipliği kaplayan yapı değildir. | Ligaz DNA parçalarını birleştirir. | DNA polimeraz III yeni bakteriyel DNA zincirini uzatır. | Topoizomeraz sarmal gerilimini giderir; tek ipliği kaplamaz.')
add(2021,75,'rep','Okazaki parçaları geciken iplikte kesintili sentezlenen DNA bölümleridir. Ligaz komşu parçaların şeker-fosfat omurgasını birleştirir. Her parça yine 5′→3′ sentezlenir.','Ligaz komşu DNA parçaları arasındaki kesintiyi kapatır. | Polimeraz DNA zincirini uzatır; son kesintiyi kapatan enzim ligazdır. | Topoizomeraz burulma gerilimini düzenler. | Helikaz çift zinciri açar. | Transkriptaz RNA sentezleyen enzimdir; Okazaki parçalarını birleştirmez.')
add(2021,76,'rep','Ökaryotik çekirdek DNA’sı interfazın S evresinde eşlenir. Mitoz evrelerinde önceden eşlenmiş kromozomlar ayrılır.','İnterfazın S evresi DNA replikasyonunun gerçekleştiği dönemdir. | Telofaz mitozun sonudur; normal genom eşlenmesi burada yapılmaz. | Anafaz kardeş kromatidlerin ayrıldığı dönemdir. | Metafaz kromozomların orta düzlemde dizildiği dönemdir. | Prometafaz iğ bağlantılarının kurulduğu mitoz evresidir.')
add(2021,77,'signal','Fosfolipaz C, PIP₂’yi DAG ve IP₃’e ayırır. DAG, protein kinaz C’nin ilgili izoformlarını etkinleştirir.','Adenilat siklaz ATP’den cAMP üretir; DAG’ın temel kinaz hedefi değildir. | PKA cAMP ile etkinleşir. | PKB/AKT başlıca PI3K-PIP₃ yolu üzerinden etkinleşir. | Fosfodiesteraz siklik nükleotidleri yıkar. | PKC DAG’ın klasik hedefidir; bazı izoformlarında Ca²⁺ de gereklidir.')
add(2021,78,'signal','Klasik steroid hormon reseptörleri sitozol veya çekirdekte bulunan hücre içi reseptörlerdir. GPCR, enzim bağlantılı ve ligand kapılı kanal reseptörleri hücre yüzeyinde bulunur.','G proteinine eşlenik reseptörler integral zar proteinleridir. | Enzim bağlantılı reseptörler membranı geçen reseptör grubudur. | Ligand kapılı iyon kanalları membran üzerinden iyon akışını düzenler. | Klasik steroid reseptörleri hücre içi reseptörlerdir. | Asetilkolinin nikotinik ve muskarinik reseptörleri hücre yüzeyindedir.')
add(2021,79,'signal','IP₃ küçük bir ikinci haberci olarak ER’den Ca²⁺ salınımını uyarır. Fosfolipaz C üretici enzim, kalmodulin ise Ca²⁺ bağlayan hedef proteindir.','Mg²⁺ birçok enzimin kofaktörüdür; burada klasik ikinci haberci olarak hedeflenmez. | Fosfolipaz C ikinci haberci üreten enzimdir. | IP₃ hücre içinde oluşan ve Ca²⁺ salınımını uyaran ikinci habercidir. | Kalmodulin Ca²⁺ bağlayan sinyal hedefi proteinidir. | mTORC2 bir protein kinaz kompleksidir; küçük ikinci haberci değildir.')
add(2021,81,'ecm','Bazal laminanın temel bileşenleri laminin, tip IV kollajen, nidogen ve perlekandır. Mast hücresi bir matriks molekülü değil canlı hücredir.','Laminin bazal laminanın ağ oluşturan glikoproteinidir. | Perlekan bazal laminada bulunan heparan sülfat proteoglikanıdır. | Nidogen laminin ve kollajen ağları arasında bağlantıya katkı sağlar. | Mast hücresi bağ dokusu hücresidir; bazal lamina bileşeni olan molekül değildir. | Tip IV kollajen bazal laminanın ağ yapısına katılır.')
add(2021,83,'rna','DNA çift sarmalında karşılıklı bazlar hidrojen bağları kurar. Aynı iplikteki nükleotidler ise kovalent fosfodiester bağlarıyla bağlıdır.','Glikozidik bağ baz ile şekeri birleştirir. | Karşı ipliklerde A–T ve G–C arasında hidrojen bağları vardır. | Peptid bağı amino asitler arasındadır. | Fosfodiester bağı aynı DNA ipliğinin omurgasındadır. | Ester bağları fosfat-şeker yapısında yer alır; baz çiftlerinin bağı hidrojen bağıdır.')
add(2021,85,'rep','Bakteriyel DNA polimeraz V, hasarı atlayarak DNA sentezine devam edebilen translezyon polimerazıdır. Bu mekanizma hataya yatkın olabilir; normal yüksek doğruluklu replikasyonla aynı değildir.','Polimeraz II onarım ve replikasyonun yeniden başlamasında görev alabilir; sorudaki klasik TLS enzimi Pol V’dir. | Polimeraz III başlıca bakteriyel replikatif polimerazdır. | Polimeraz V hasarlı kalıp üzerinden translezyon sentez yapabilir. | DNA glikozilaz hasarlı bazı çıkarır; DNA sentezleyen enzim değildir. | Helikaz DNA açar; nükleotid ekleyerek hasar atlamaz.')
add(2021,87,'rep','MSH2 ve MLH1 yanlış eşleşme onarımının bileşenleridir. Bu sistemin kalıtsal bozuklukları Lynch sendromu/HNPCC ile ilişkilidir.','Transkripsiyona eşlenik onarım RNA polimerazı durduran lezyonlarla ilişkilidir. | MSH2 ve MLH1 replikasyon sonrası yanlış eşleşme onarımında görev alır. | Baz eksizyonu tek hasarlı bazların glikozilazlarla çıkarılmasıyla başlar. | Nükleotid eksizyonu hacimli DNA lezyonlarıyla ilişkilidir. | Çift zincir kırığı onarımı homolog rekombinasyon veya uç birleştirme yollarıyla yapılır.')
add(2021,88,'translation','tRNA bir ucunda amino asit, antikodon bölgesinde ise mRNA kodonuna uygun tanıma dizisi taşır. Böylece genetik şifre ile amino asit arasında adaptörlük yapar.','siRNA RNA susturulmasında görev alır. | mRNA amino asit sırasını belirleyen kodonları taşır. | tRNA amino asitleri ribozoma getiren adaptördür. | rRNA ribozomun yapısal ve katalitik bileşenidir. | shRNA gen susturulmasında kullanılan saç tokası biçimli RNA’dır.')
add(2021,89,'rna','XIST uzun kodlamayan RNA, inaktive olacak X kromozomu üzerinde birikerek susturucu kromatin oluşmasına yardım eder. Protein kodlayan bir mRNA değildir.','XIST X kromozomu inaktivasyonunun temel düzenleyici RNA’sıdır. | mRNA protein kodlayan mesaj RNA’sıdır. | sgRNA CRISPR sisteminde hedefleme rehberi olabilir. | tRNA amino asit taşır. | miRNA hedef mRNA’ların ifadesini baskılar; XIST’in kromozom kaplama işlevini tanımlamaz.')
add(2021,90,'nuc','Histon metilasyonunun etkisi işaretlenen amino asit ve konumuna bağlıdır. Bazı işaretler aktif, bazıları baskılanmış kromatinle ilişkilidir; “her zaman” baskılar denemez.','Yoğun heterokromatin DNA’ya erişimi genel olarak azaltır. | Metilasyonun sonucu kalıntıya bağlıdır; her durumda baskılanma olmaz. | Histon deasetilazlar represör komplekslerine katılabilir. | Gevşek ökromatin aktif transkripsiyona daha elverişlidir. | Histon asetilasyonu genel olarak erişilebilir ve aktif kromatinle ilişkilidir.')
add(2021,91,'rna','Ökaryotik RNA polimeraz II promotörde genel transkripsiyon faktörleriyle başlangıç kompleksi kurar. Enhancer ve represörler düzenler; temel başlangıç düzeneğinin yerine geçmez.','Genel transkripsiyon faktörleri Pol II’nin promotörde toplanması ve başlaması için gereklidir. | Enhancerlar etkinliği artırabilir; her genin temel başlatılması için aynı enhancer gerekmez. | Represörler baskılar; başlatmayı sağlayan genel gereksinim değildir. | Konsensus DNA dizisi bir bağlanma bölgesi tanımıdır; başlatıcı faktörlerin yerini tutmaz. | Cis düzenleyici diziler DNA bölgeleridir; sorudaki gerekli protein grubu transkripsiyon faktörleridir.')
add(2021,93,'lab','Western blot proteinleri ayırıp özgül antikorla saptar. Aynı deney koşullarında yükleme kontrolüyle bant şiddeti karşılaştırılarak protein miktarındaki göreli değişim değerlendirilebilir.','PCR nükleik asit çoğaltır; protein miktarını doğrudan ölçmez. | Western blot belirli proteinin bant sinyalini karşılaştırmaya uygundur. | Southern blot DNA’yı saptar. | Agaroz elektroforezi başlıca nükleik asit ayrımı için kullanılır. | Northern blot RNA’yı saptar.')
add(2021,94,'lab','ChIP, belirli bir proteine bağlı DNA bölgelerini antikorla zenginleştirerek protein-DNA ilişkisini araştırır. Hücresel boyama yöntemleri tek başına belirli DNA bölgesine bağlanmayı göstermez.','ChIP hedef proteine bağlı kromatini immünopresipitasyonla toplar. | İmmünofloresan protein yerleşimini gösterebilir; tek başına belirli DNA bağlanmasını kanıtlamaz. | İmmünohistokimya doku içindeki antijen dağılımını gösterir. | Northern blot RNA’yı inceler. | Southern blot DNA dizilerini saptar; tek başına protein-DNA etkileşim testi değildir.')

def finish():
    pending=[q['id'] for k,q in Q.items() if k not in DATA and k not in OMIT]
    assert not pending, f'Değerlendirilmemiş {len(pending)} soru: {pending[:8]}'
    data={Q[k]['id']:v for k,v in sorted(DATA.items())}
    omitted=[{'id':Q[k]['id'],'year':Q[k]['year'],'number':k[1],'reason':v} for k,v in sorted(OMIT.items())]
    used={t:G[t] for d in data.values() for t in d['terms']}
    manifest={'schemaVersion':1,'scope':'Dönem 1 / 2. Kurul','mode':'static_authored','total':len(Q),'supported':len(data),'omitted':len(omitted),'pending':len(pending),'policy':'Eksik veya tartışmalı sorulara AI eklenmez. Kaynak soru ve anahtar değişmez. AI açıklaması akademik doğrulama değildir.','questionsSha256':hashlib.sha256(json.dumps(questions,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),'excluded':omitted}
    out=ROOT/'js/data/archive/ai-support-kurul2.js'
    out.write_text('// AI desteği; kaynak sorular ve anahtarlar değiştirilmez.\nwindow.ARCHIVE_EXPLANATIONS = '+json.dumps(data,ensure_ascii=False,indent=2)+';\nwindow.ARCHIVE_GLOSSARY = '+json.dumps(used,ensure_ascii=False,indent=2)+';\nwindow.ARCHIVE_AI_MANIFEST = '+json.dumps(manifest,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
    reportdir=ROOT/'_work/ai-kurul2'
    reportdir.mkdir(parents=True,exist_ok=True)
    (reportdir/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    review=['# AI desteği kapsamı','',f'{len(Q)} soru değerlendirildi. {len(data)} soruya destek eklendi, {len(omitted)} soruya eklenmedi.','', 'Bu liste editoryal AI değerlendirmesidir; kaynak kurumun düzeltmesi veya akademik doğrulama değildir.','', '| Yıl | Soru | Eklenmeme gerekçesi |','|---|---:|---|']
    review.extend(f"| {x['year']} | {x['number']} | {x['reason']} |" for x in omitted)
    (ROOT/'docs/AI_KURUL2_KONTROL.md').write_text('\n'.join(review)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in manifest.items() if k!='excluded'},ensure_ascii=False))

if __name__=='__main__':
    # Yıl dosyaları aynı editoryal bağlamı paylaşır.
    for name in ['year2022.py','year2023.py','year2024.py','year2025.py','exclusions.py']:
        exec((pathlib.Path(__file__).parent/name).read_text(encoding='utf-8'),globals())
    finish()
