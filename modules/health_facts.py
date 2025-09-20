"""
Daily Health Facts and Ayurvedic Tips
Rotating educational content for patients
"""

import random
from datetime import datetime

AYURVEDIC_HEALTH_FACTS = [
    {
        'title': 'Golden Milk Benefits',
        'fact': 'Turmeric milk (Haldi Doodh) before bedtime helps reduce inflammation and promotes better sleep naturally.',
        'category': 'Ayurvedic Remedies'
    },
    {
        'title': 'Morning Routine',
        'fact': 'Drinking warm water with lemon and honey on empty stomach helps detoxify liver and boost metabolism.',
        'category': 'Daily Wellness'
    },
    {
        'title': 'Digestive Health',
        'fact': 'Eating your largest meal at lunchtime (12-2 PM) when digestive fire (Agni) is strongest improves digestion.',
        'category': 'Digestion'
    },
    {
        'title': 'Stress Relief',
        'fact': 'Pranayama (breathing exercises) for just 5 minutes daily can reduce stress and lower blood pressure naturally.',
        'category': 'Mental Health'
    },
    {
        'title': 'Immunity Booster',
        'fact': 'Chyawanprash with warm milk increases immunity and provides essential vitamins for all age groups.',
        'category': 'Immunity'
    },
    {
        'title': 'Sleep Quality',
        'fact': 'Massaging feet with sesame oil before bed (Padabhyanga) promotes deep sleep and reduces anxiety.',
        'category': 'Sleep & Rest'
    },
    {
        'title': 'Skin Health',
        'fact': 'Rose water and sandalwood paste as a face mask helps maintain healthy, glowing skin naturally.',
        'category': 'Beauty & Skin'
    },
    {
        'title': 'Joint Health',
        'fact': 'Regular consumption of ginger tea helps reduce joint pain and inflammation in arthritis patients.',
        'category': 'Joint Care'
    },
    {
        'title': 'Weight Management',
        'fact': 'Drinking cumin water (Jeera water) 30 minutes before meals helps boost metabolism and aids weight loss.',
        'category': 'Weight Management'
    },
    {
        'title': 'Heart Health',
        'fact': 'Arjuna bark tea is excellent for heart health and helps maintain healthy cholesterol levels naturally.',
        'category': 'Cardiovascular'
    },
    {
        'title': 'Mental Clarity',
        'fact': 'Brahmi (Bacopa) herb enhances memory, concentration, and overall brain function when taken regularly.',
        'category': 'Brain Health'
    },
    {
        'title': 'Seasonal Health',
        'fact': 'During monsoon, consume warm, cooked foods and avoid raw salads to maintain digestive health.',
        'category': 'Seasonal Care'
    },
    {
        'title': 'Hydration',
        'fact': 'Room temperature water is better than cold water for digestion according to Ayurvedic principles.',
        'category': 'Hydration'
    },
    {
        'title': 'Energy Levels',
        'fact': 'Ashwagandha with warm milk at bedtime helps combat fatigue and increases energy levels naturally.',
        'category': 'Energy & Vitality'
    },
    {
        'title': 'Detoxification',
        'fact': 'Weekly oil massage (Abhyanga) with warm sesame oil helps eliminate toxins and improves circulation.',
        'category': 'Detox'
    }
]

GENERAL_HEALTH_TIPS = [
    {
        'title': 'Water Intake',
        'fact': 'Drinking 8-10 glasses of water daily helps maintain kidney function and keeps skin healthy.',
        'category': 'Hydration'
    },
    {
        'title': 'Walking Benefits',
        'fact': 'A 30-minute daily walk reduces risk of heart disease by 40% and improves mental health.',
        'category': 'Exercise'
    },
    {
        'title': 'Meditation',
        'fact': 'Just 10 minutes of daily meditation can reduce stress hormones and improve immune function.',
        'category': 'Mental Wellness'
    },
    {
        'title': 'Nutrition',
        'fact': 'Eating 5 servings of fruits and vegetables daily provides essential vitamins and reduces disease risk.',
        'category': 'Nutrition'
    },
    {
        'title': 'Sleep Importance',
        'fact': '7-8 hours of quality sleep is essential for memory consolidation and cellular repair.',
        'category': 'Sleep'
    }
]

def get_daily_health_fact():
    """Get a random health fact for the day"""
    all_facts = AYURVEDIC_HEALTH_FACTS + GENERAL_HEALTH_TIPS
    
    # Use date as seed for consistent daily fact
    today = datetime.now().strftime('%Y-%m-%d')
    random.seed(today)
    
    return random.choice(all_facts)

def get_random_health_fact():
    """Get a completely random health fact"""
    all_facts = AYURVEDIC_HEALTH_FACTS + GENERAL_HEALTH_TIPS
    return random.choice(all_facts)

def get_health_facts_by_category(category):
    """Get health facts by specific category"""
    all_facts = AYURVEDIC_HEALTH_FACTS + GENERAL_HEALTH_TIPS
    return [fact for fact in all_facts if fact['category'].lower() == category.lower()]

def get_ayurvedic_tip_of_day():
    """Get daily Ayurvedic tip"""
    today = datetime.now().strftime('%Y-%m-%d')
    random.seed(today)
    return random.choice(AYURVEDIC_HEALTH_FACTS)