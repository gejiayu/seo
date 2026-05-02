#!/usr/bin/env python3
"""
生成翻译任务分配列表
每个agent负责处理约12个类别目录
"""

import json
from pathlib import Path

categories = [
    "agricultural-farming-rental-tools",
    "agriculture-farming-tools",
    "ai-marketing",
    "ai-productivity",
    "airport-aviation-management-tools",
    "architecture-design-tools",
    "audio-video-equipment-rental-tools",
    "auto-dealer-management-tools",
    "automotive-dealer-dms-tools",
    "automotive-repair-tools",
    "banking-financial-services-tools",
    "beauty-salon-tools",
    "bike-cycling-rental-tools",
    "blue-collar-tools",
    "boat-marine-rental-tools",
    "camera-photography-rental-tools",
    "camping-outdoor-gear-rental-tools",
    "car-vehicle-rental-tools",
    "casino-gaming-entertainment-tools",
    "child-care-preschool-tools",
    "cleaning-maintenance-rental-tools",
    "construction-building-rental-tools",
    "construction-contractor-tools",
    "costume-fashion-rental-tools",
    "coworking-space-management-tools",
    "customer-support-tools",
    "cybersecurity-it-security-tools",
    "dental-medical-practice-tools",
    "diving-water-sports-rental-tools",
    "ecommerce-selling-tools",
    "education-lms-platform-tools",
    "education-tools",
    "education-training-tools",
    "energy-environmental-tools",
    "energy-utilities-management",
    "entertainment-media-production-tools",
    "event-planning-tools",
    "finance-accounting-tools",
    "fishing-gear-rental-tools",
    "fitness-gym-management",
    "florist-flower-shop-tools",
    "food-beverage-distribution-tools",
    "franchise-business-tools",
    "furniture-home-rental-tools",
    "generator-power-rental-tools",
    "golf-equipment-rental-tools",
    "government-public-sector-tools",
    "healthcare-medical-tools",
    "healthcare-medical-treatment-tools",
    "healthcare-wellness-tools",
    "hiking-climbing-gear-rental-tools",
    "home-services-renovation",
    "hospitality-restaurant-pos-tools",
    "hr-recruitment-onboarding-tools",
    "hr-recruitment-tools",
    "insurance-agency-tools",
    "insurance-claims-processing-tools",
    "jewelry-watch-retail-tools",
    "kitchen-cooking-rental-tools",
    "landscaping-grounds-maintenance",
    "laundry-dry-cleaning-tools",
    "legal",
    "legal-compliance-tools",
    "legal-document-management-tools",
    "lighting-lamp-rental-tools",
    "logistics-supply-chain-tools",
    "logistics-warehouse-management-tools",
    "machinery-heavy-equipment-rental-tools",
    "manufacturing-production-tools",
    "manufacturing-quality-control-tools",
    "maritime-shipping-tools",
    "massage-spa-wellness-tools",
    "medical-equipment-rental-tools",
    "mining-extraction-tools",
    "music-audio-production",
    "nonprofit-charity-tools",
    "optometry-eye-care-tools",
    "paintball-laser-tag-rental-tools",
    "party-event-supplies-rental-tools",
    "pet-services-tools",
    "pet-store-pet-supply-tools",
    "pet-vet-clinic-tools",
    "pharmaceutical-life-sciences-tools",
    "photography-video-production",
    "portable-sanitation-rental-tools",
    "print-graphic-design-tools",
    "professional-services-tools",
    "publishing-media-tools",
    "real-estate-agent-tools",
    "real-estate-property-tools",
    "religious-nonprofit-organization-tools",
    "remote-tools",
    "renewable-energy-management-tools",
    "restaurant-food-service-tools",
    "retail-ecommerce-operations-tools",
    "retail-pos-inventory-tools",
    "scooter-moped-rental-tools",
    "security-surveillance-rental-tools",
    "ski-snowboard-rental-tools",
    "sporting-goods-retail-tools",
    "sports-equipment-rental-tools",
    "sports-fitness-tools",
    "sports-recreation-management",
    "staffing-recruitment-agency-tools",
    "staging-rigging-rental-tools",
    "storage-unit-rental-tools",
    "subscription-recurring-billing-tools",
    "telecommunications-network-tools",
    "tennis-racket-rental-tools",
    "tent-canopy-rental-tools",
    "tool-hardware-rental-tools",
    "transportation-fleet-tools",
    "travel-agency-tour-operator-tools",
    "travel-hospitality-tools",
    "vending-machine-management-tools",
    "warehouse-inventory-tools",
    "wedding-event-rental-tools",
    "wine-spirits-liquor-store-tools",
]

# 分配给10个agent
agents = {}
for i in range(10):
    start = i * 12
    end = start + 12 if i < 9 else len(categories)
    agents[f"agent-{i+1}"] = categories[start:end]

# 输出分配结果
for agent_name, agent_categories in agents.items():
    print(f"{agent_name}: {len(agent_categories)} categories")
    for cat in agent_categories:
        print(f"  - {cat}")
    print()

# 保存到JSON文件
with open("scripts/translation_tasks.json", "w", encoding="utf-8") as f:
    json.dump(agents, f, ensure_ascii=False, indent=2)

print("Translation tasks saved to scripts/translation_tasks.json")