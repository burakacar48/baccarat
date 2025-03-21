#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tahmin Motoru
-----------
Tüm algoritmaları ve derin öğrenme modelini koordine eden ana tahmin motoru.
"""

import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)

class PredictionEngine:
    """
    Tahmin Motoru
    
    Tüm algoritmaları ve derin öğrenme modelini yöneterek tahmin üretir.
    """
    
    def __init__(self):
        """
        PredictionEngine sınıfını başlatır
        """
        self.algorithms = []  # Kayıtlı algoritmaların listesi
        self.deep_learning_model = None  # LSTM modeli
        self.result_aggregator = None  # Sonuç birleştirici
        self.db_manager = None  # Veritabanı yöneticisi
        
        logger.info("Tahmin motoru başlatıldı")
    
    def register_algorithm(self, algorithm):
        """
        Bir algoritma kaydeder
        
        Args:
            algorithm: Algoritma nesnesi (BaseAlgorithm'dan türetilmiş)
        """
        self.algorithms.append(algorithm)
        logger.info(f"Algoritma kaydedildi: {algorithm.name}")
    
    def set_deep_learning_model(self, model):
        """
        Derin öğrenme modelini ayarlar
        
        Args:
            model: LSTM model nesnesi
        """
        self.deep_learning_model = model
        logger.info("Derin öğrenme modeli ayarlandı")
    
    def set_result_aggregator(self, aggregator):
        """
        Sonuç birleştiriciyi ayarlar
        
        Args:
            aggregator: ResultAggregator nesnesi
        """
        self.result_aggregator = aggregator
        logger.info("Sonuç birleştirici ayarlandı")
    
    def set_db_manager(self, db_manager):
        """
        Veritabanı yöneticisini ayarlar
        
        Args:
            db_manager: DatabaseManager nesnesi
        """
        self.db_manager = db_manager
        logger.info("Veritabanı yöneticisi ayarlandı")
    
    
    def predict(self, data=None, save_prediction=True):
        # Veri yoksa veritabanından son verileri getir
        if data is None:
            if not self.db_manager:
                logger.error("Veritabanı yöneticisi bulunamadı. Veri sağlayın veya DB yöneticisi ayarlayın.")
                return None
            
            # Her seferinde yeni bir bağlantı oluştur
            db_connection = self.db_manager._get_connection()
            cursor = db_connection.cursor()
            
            # Son N sonucu getir
            cursor.execute("SELECT * FROM game_results ORDER BY id DESC LIMIT 20")
            last_results = cursor.fetchall()
            
            if not last_results:
                logger.warning("Veritabanında sonuç bulunamadı. Tahmin yapılamıyor.")
                return None
            
            # Sonuçları düzenle
            results = [result['result'] for result in last_results]
            results.reverse()  # En eskiden en yeniye sırala
            
            data = {'last_results': results}
        
        # Geri kalan kod aynı kalacak
        
        # Sonuç kaydı için her seferinde yeni bir bağlantı kullan
        if save_prediction and self.db_manager:
            try:
                db_connection = self.db_manager._get_connection()
                cursor = db_connection.cursor()
                
                # Algoritma ve tahmin kaydetme kodları buraya
                # Her seferinde yeni bir bağlantı kullanılacak
            except Exception as e:
                logger.error(f"Tahmin kaydetme hatası: {str(e)}")

    
    def update_results(self, actual_result):
        """
        Gerçek sonucu kaydeder ve algoritma performanslarını günceller
        
        Args:
            actual_result (str): Gerçekleşen sonuç (P/B/T)
        
        Returns:
            int: Eklenen sonuç kaydının ID'si, hata durumunda -1
        """
        if not self.db_manager:
            logger.error("Veritabanı yöneticisi bulunamadı. Sonuç kaydedilemedi.")
            return -1
        
        try:
            # Son tahminleri getir
            # Gerçek uygulamada burada aktif tahminleri almanız gerekebilir
            
            # Sonucu kaydet
            result_id = self.db_manager.save_result(
                result=actual_result,
                timestamp=datetime.now().isoformat(),
                previous_pattern=None,  # Burada önceki deseninizi ekleyebilirsiniz
                session_id=1  # Aktif oturum ID'si
            )
            
            # Algoritma performanslarını güncelle
            # Gerçek uygulamada burada algoritma tahminlerini ve gerçek sonucu karşılaştırmanız gerekir
            
            logger.info(f"Sonuç kaydedildi: ID={result_id}, Sonuç={actual_result}")
            return result_id
        except Exception as e:
            logger.error(f"Sonuç güncelleme hatası: {str(e)}")
            return -1
    
    def get_algorithm_stats(self):
        """
        Tüm algoritmaların istatistiklerini getirir
        
        Returns:
            list: Algoritma istatistiklerinin listesi
        """
        stats = []
        
        for algorithm in self.algorithms:
            stats.append(algorithm.get_info())
        
        # Derin öğrenme modeli istatistiklerini ekle
        if self.deep_learning_model and hasattr(self.deep_learning_model, 'trained'):
            stats.append({
                'name': 'LSTM',
                'weight': 1.5,  # Varsayılan ağırlık
                'accuracy': getattr(self.deep_learning_model, 'accuracy', 0.0),
                'trained': self.deep_learning_model.trained,
                'model_version': getattr(self.deep_learning_model, 'version', '1.0')
            })
        
        return stats