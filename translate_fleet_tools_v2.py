#!/usr/bin/env python3
"""
Translate Chinese JSON files to proper English content.
Uses contextual translation instead of word-by-word replacement.
"""

import json
import re
from pathlib import Path

def translate_title(title_zh):
    """Translate title with proper English formatting."""
    # Pattern: 2026年XXX评测：YYY
    # Result: 2026 XXX Review: YYY

    translations = {
        "2026年最佳车队管理软件评测：GPS定位与车辆调度全攻略":
            "Best Fleet Management Software 2026: GPS Tracking & Vehicle Dispatch Complete Guide",
        "2026年冷链车队监控评测：温度追踪与货物安全保障":
            "Cold Chain Fleet Monitoring 2026: Temperature Tracking & Cargo Safety Solutions",
        "2026年司机管理与安全系统评测：行为监控与合规性保障":
            "Driver Management & Safety Systems 2026: Behavior Monitoring & Compliance Solutions",
        "2026年电子日志ELD软件评测：合规性与效率优化":
            "Electronic Logging Device (ELD) Software 2026: Compliance & Efficiency Optimization",
        "2026年电动车车队管理评测：充电与续航优化":
            "Electric Vehicle Fleet Management 2026: Charging & Range Optimization",
        "车队资产管理软件评测：车辆全生命周期管理":
            "Fleet Asset Management Software Review: Vehicle Lifecycle Management",
        "车队绩效基准工具评测：数据驱动决策":
            "Fleet Benchmarking Performance Tools: Data-Driven Decision Making",
        "车队预算规划工具评测：成本预测与管控":
            "Fleet Budget Planning Tools Review: Cost Forecasting & Control",
        "车队碳足迹追踪评测：排放监控与合规":
            "Fleet Carbon Footprint Tracking Review: Emission Monitoring & Compliance",
        "车队冷链监控评测：温度追踪与食品安全":
            "Fleet Cold Chain Monitoring Review: Temperature Tracking & Food Safety",
        "车队合规管理软件评测：法规遵循与风险管控":
            "Fleet Compliance Management Software Review: Regulatory Compliance & Risk Control",
        "车队成本优化工具评测：降本增效策略":
            "Fleet Cost Optimization Tools Review: Cost Reduction Strategies",
        "跨境车队管理工具评测：国际运输合规":
            "Cross-Border Fleet Management Tools: International Transport Compliance",
        "车队客户服务支持评测：响应与满意度优化":
            "Fleet Customer Service Support Review: Response & Satisfaction Optimization",
        "车队客户服务工具评测：沟通与支持平台":
            "Fleet Customer Service Tools Review: Communication & Support Platforms",
        "车队数据导出集成工具评测：系统对接与数据流转":
            "Fleet Data Export Integration Tools: System Integration & Data Flow",
        "车队数字化转型平台评测：智能化升级路径":
            "Fleet Digital Transformation Platforms: Smart Upgrade Solutions",
        "车队处置转卖管理评测：资产处置与残值优化":
            "Fleet Disposal & Resale Management Review: Asset Disposal & Residual Value",
        "车队档案数字化管理评测：文档存储与检索":
            "Fleet Document Digital Management: Document Storage & Retrieval",
        "车队文档管理系统评测：电子化与合规":
            "Fleet Document Management Systems: Digitization & Compliance",
        "车队司机福利管理评测：激励与留存策略":
            "Fleet Driver Benefits Management Review: Incentive & Retention Strategies",
        "车队司机沟通平台评测：即时通讯与协作":
            "Fleet Driver Communication Platforms: Instant Messaging & Collaboration",
        "车队司机沟通工具评测：信息传递与反馈":
            "Fleet Driver Communication Tools: Information Transfer & Feedback",
        "车队司机疲劳监控评测：安全预警与干预":
            "Fleet Driver Fatigue Monitoring Review: Safety Alerts & Intervention",
        "车队司机移动App评测：便携管理与操作":
            "Fleet Driver Mobile Apps Review: Portable Management & Operations",
        "车队司机离职工具评测：流程标准化与合规":
            "Fleet Driver Offboarding Tools: Process Standardization & Compliance",
        "车队司机入职工具评测：培训与合规流程":
            "Fleet Driver Onboarding Tools Review: Training & Compliance Process",
        "车队司机薪酬结算评测：薪资计算与发放":
            "Fleet Driver Payroll Settlement Review: Salary Calculation & Payment",
        "车队司机薪酬管理评测：薪资体系与激励":
            "Fleet Driver Payroll & Compensation Review: Salary Structure & Incentives",
        "车队司机绩效分析评测：数据驱动的评价体系":
            "Fleet Driver Performance Analytics: Data-Driven Evaluation System",
        "车队司机绩效评分评测：量化考核与激励":
            "Fleet Driver Performance Scorecards: Quantitative Assessment & Incentives",
        "车队司机招聘平台评测：人才获取与筛选":
            "Fleet Driver Recruitment Platforms: Talent Acquisition & Screening",
        "车队司机留存激励评测：人才保留策略":
            "Fleet Driver Retention Engagement Review: Talent Retention Strategies",
        "车队司机安全培训工具评测：技能提升与事故预防":
            "Fleet Driver Safety Coaching Tools: Skill Enhancement & Accident Prevention",
        "车队司机评分分析评测：行为监控与改进":
            "Fleet Driver Scorecard Analytics: Behavior Monitoring & Improvement",
        "车队司机培训平台评测：技能提升与合规":
            "Fleet Driver Training Platforms: Skill Enhancement & Compliance",
        "车队司机车辆匹配评测：资源优化与调度":
            "Fleet Driver Vehicle Matching: Resource Optimization & Dispatch",
        "车队应急响应系统评测：事故处理与快速反应":
            "Fleet Emergency Response Systems: Accident Handling & Quick Response",
        "车队财务管理工具评测：成本核算与预算":
            "Fleet Financial Management Tools: Cost Accounting & Budgeting",
        "车队规模优化评测：资源配置与效率":
            "Fleet Sizing Optimization: Resource Allocation & Efficiency",
        "车队货运可视平台评测：货物追踪与透明度":
            "Fleet Freight Visibility Platforms: Cargo Tracking & Transparency",
        "车队加油卡计划评测：成本管控与消费分析":
            "Fleet Fuel Card Programs: Cost Control & Consumption Analysis",
        "车队地理围栏工具评测：区域监控与管理":
            "Fleet Geofencing Location Tools: Zone Monitoring & Management",
        "车队地理围栏管理评测：区域划分与报警":
            "Fleet Geofencing Zone Management: Zone Division & Alerts",
        "车队危险品运输评测：合规与安全管理":
            "Fleet Hazardous Materials Transport: Compliance & Safety Management",
        "车队事故管理评测：报告流程与预防":
            "Fleet Incident Accident Management: Reporting Process & Prevention",
        "车队保险风险管理评测：成本控制与理赔":
            "Fleet Insurance Risk Management: Cost Control & Claims",
        "车队集成API平台评测：系统对接与数据流转":
            "Fleet Integration API Platforms: System Integration & Data Flow",
        "车队IoT传感器遥测评测：数据采集与监控":
            "Fleet IoT Sensors Telematics: Data Collection & Monitoring",
        "车队末端配送追踪评测：实时定位与客户通知":
            "Fleet Last Mile Delivery Tracking: Real-time Location & Customer Notification",
        "车队货运板平台评测：货源匹配与调度":
            "Fleet Load Board Platforms: Cargo Matching & Dispatch",
        "车队装载规划软件评测：效率优化与成本降低":
            "Fleet Load Planning Software: Efficiency Optimization & Cost Reduction",
        "2026年车队维护软件评测：预防性保养与成本控制":
            "Fleet Maintenance Software 2026: Preventive Maintenance & Cost Control",
        "车队经理仪表盘平台评测：数据可视化与决策":
            "Fleet Manager Dashboard Platforms: Data Visualization & Decision Making",
        "车队司机移动工具评测：便携管理与操作":
            "Fleet Mobile App Driver Tools: Portable Management & Operations",
        "车队多站点路线软件评测：路径优化与效率":
            "Fleet Multi Stop Routing Software: Route Optimization & Efficiency",
        "车队入职培训平台评测：快速上岗与合规":
            "Fleet Onboard Training Platforms: Quick Onboarding & Compliance",
        "车队配件库存管理评测：库存控制与采购":
            "Fleet Parts Inventory Management: Inventory Control & Purchasing",
        "车队预测性维护AI评测：故障预测与预防":
            "Fleet Predictive Maintenance AI: Failure Prediction & Prevention",
        "车队实时报警系统评测：即时预警与响应":
            "Fleet Real Time Alert Systems: Instant Alerts & Response",
        "车队实时追踪平台评测：定位监控与数据":
            "Fleet Real Time Tracking Platforms: Location Monitoring & Data",
        "车队租赁管理评测：车辆租赁与合同":
            "Fleet Rental Leasing Management: Vehicle Rental & Contracts",
        "车队报表分析工具评测：数据可视化与决策":
            "Fleet Reporting Analytics Tools: Data Visualization & Decision Making",
        "车队安防防盗系统评测：车辆安全与监控":
            "Fleet Security Anti Theft Systems: Vehicle Safety & Monitoring",
        "车队排班管理评测：调度优化与效率":
            "Fleet Shift Scheduling Management: Dispatch Optimization & Efficiency",
        "车队规格配置工具评测：标准化与效率":
            "Fleet Specification Configuration Tools: Standardization & Efficiency",
        "车队订阅管理工具评测：订阅服务与账单":
            "Fleet Subscription Management Tools: Subscription Services & Billing",
        "车队税务IFTA报告工具评测：合规与计算":
            "Fleet Tax IFTA Reporting Tools: Compliance & Calculation",
        "车队轮胎管理软件评测：磨损监控与更换":
            "Fleet Tire Management Software: Wear Monitoring & Replacement",
        "车队交通路线优化评测：路径规划与效率":
            "Fleet Traffic Route Optimization: Route Planning & Efficiency",
        "车队车辆采购管理评测：采购流程与成本":
            "Fleet Vehicle Acquisition Procurement: Purchase Process & Costs",
        "车队车辆采购工具评测：购置决策与资源":
            "Fleet Vehicle Acquisition Tools: Purchase Decisions & Resources",
        "车队车辆分配工具评测：资源优化与调度":
            "Fleet Vehicle Assignment Tools: Resource Optimization & Dispatch",
        "车队车辆互联平台评测：数据共享与集成":
            "Fleet Vehicle Connectivity Platforms: Data Sharing & Integration",
        "车队车辆处置退役评测：报废流程与合规":
            "Fleet Vehicle Disposal Retirement: Scrapping Process & Compliance",
        "车队车辆健康监控评测：故障预警与维护":
            "Fleet Vehicle Health Monitoring: Failure Alerts & Maintenance",
        "车队车辆检查软件评测：检查流程与合规":
            "Fleet Vehicle Inspection Software: Inspection Process & Compliance",
        "车队车辆生命周期管理评测：全流程管理":
            "Fleet Vehicle Lifecycle Management: Full-Process Management",
        "车队车辆绩效基准评测：数据对比与分析":
            "Fleet Vehicle Performance Benchmarking: Data Comparison & Analysis",
        "车队车辆注册管理评测：登记流程与合规":
            "Fleet Vehicle Registration Management: Registration Process & Compliance",
        "车队车辆注册工具评测：登记流程与效率":
            "Fleet Vehicle Registration Tools: Registration Process & Efficiency",
        "车队车辆更换规划评测：更换周期与成本":
            "Fleet Vehicle Replacement Planning: Replacement Cycle & Costs",
        "车队车辆转售价值分析评测：残值评估与处置":
            "Fleet Vehicle Resale Value Analysis: Residual Value Assessment & Disposal",
        "车队车辆规格工具评测：配置管理标准化":
            "Fleet Vehicle Specification Tools: Configuration Management Standardization",
        "车队车辆遥测系统评测：数据采集与分析":
            "Fleet Vehicle Telematics Systems: Data Collection & Analysis",
        "车队车辆利用率分析评测：资源优化与效率":
            "Fleet Vehicle Utilization Analysis: Resource Optimization & Efficiency",
        "车队车辆保修管理评测：保修流程与索赔":
            "Fleet Vehicle Warranty Management: Warranty Process & Claims",
        "车队视频监控系统评测：安全监控与证据":
            "Fleet Video Surveillance Systems: Safety Monitoring & Evidence",
        "车队仓库场站管理评测：场地管理与调度":
            "Fleet Warehouse Yard Management: Site Management & Dispatch",
        "车队人力资源管理工具评测：员工管理与绩效":
            "Fleet Workforce Management Tools: Employee Management & Performance",
        "货运经纪管理软件评测：货源匹配与调度":
            "Freight Brokerage Management Software: Cargo Matching & Dispatch",
        "货运费率管理工具评测：定价策略与成本":
            "Freight Rate Management Tools: Pricing Strategy & Costs",
        "油耗监控管理工具评测：成本管控与优化":
            "Fuel Monitoring Management Tools: Cost Control & Optimization",
        "2026年GPS追踪系统对比：定位精度与功能":
            "GPS Tracking Systems Comparison 2026: Location Accuracy & Features",
        "重型设备车队管理评测：工程机械与调度":
            "Heavy Equipment Fleet Management: Construction Machinery & Dispatch",
        "末端配送车队工具评测：配送效率与客户":
            "Last Mile Delivery Fleet Tools: Delivery Efficiency & Customer Service",
        "运输CRM软件评测：客户管理与销售":
            "Transportation CRM Software 2026: Customer Management & Sales",
        "卡车调度软件评测：路线优化与效率":
            "Trucking Dispatch Software: Route Optimization & Efficiency",
        "车辆调度排程工具评测：调度优化与效率":
            "Vehicle Dispatch Scheduling Tools: Dispatch Optimization & Efficiency",
        "车辆检查DVIR软件评测：检查流程与合规":
            "Vehicle Inspection DVIR Software: Inspection Process & Compliance",
    }

    return translations.get(title_zh, title_zh)

def translate_description(desc_zh):
    """Translate description with proper English."""
    # Common patterns in descriptions
    patterns = [
        (r"深度评测(.+)等\d+款(.+)，对比(.+)功能，(.+)。了解更多功能和价格对比，找到最适合你的方案！专业评测助你决策！",
         r"In-depth review of \1 and other top tools, comparing \3 features. \4. Learn more about features and pricing comparison to find the best solution for you! Professional reviews to help you decide!"),
        (r"深度评测(.+)、(.+)、(.+)等\d+款(.+)，对比(.+)功能，(.+)。了解更多功能和价格对比，找到最适合你的方案！专业评测助你决策！",
         r"In-depth review of \1, \2, \3 and other top tools, comparing \5 features. \6. Learn more about features and pricing comparison to find the best solution for you! Professional reviews to help you decide!"),
    ]

    # Apply patterns
    for pattern, replacement in patterns:
        desc_zh = re.sub(pattern, replacement, desc_zh)

    # Manual translations for specific descriptions
    translations = {
        "深度评测Samsara、Geotab、Fleetio等10款车队管理软件，对比GPS追踪、车辆调度、油耗监控功能，助力运输企业降本增效。了解更多功能和价格对比，找到最适合你的方案！专业评测助你决策！":
            "In-depth review of Samsara, Geotab, Fleetio and 10 other fleet management software tools, comparing GPS tracking, vehicle dispatch, and fuel monitoring features to help transportation companies reduce costs and improve efficiency. Learn more about features and pricing comparison to find the best solution for you! Professional reviews to help you decide!",
        "深度评测Samsara、ThermoKing、Carrier等冷链监控方案，对比温度追踪、报警系统、合规报告功能，确保冷链运输安全。了解更多功能和价格对比，找到最适合你的方案！专业评测助你决策！":
            "In-depth review of Samsara, ThermoKing, Carrier and other cold chain monitoring solutions, comparing temperature tracking, alarm systems, and compliance reporting features to ensure cold chain transport safety. Learn more about features and pricing comparison to find the best solution for you! Professional reviews to help you decide!",
        "深度评测Motive、Samsara、Lytx等司机安全管理系统，对比行为监控、安全评分、合规培训功能，降低车队事故风险。了解更多功能和价格对比，找到最适合你的方案！专业评测助你决策！":
            "In-depth review of Motive, Samsara, Lytx and other driver safety management systems, comparing behavior monitoring, safety scoring, and compliance training features to reduce fleet accident risk. Learn more about features and pricing comparison to find the best solution for you! Professional reviews to help you decide!",
    }

    return translations.get(desc_zh, desc_zh)

def translate_json_file(filepath):
    """Translate JSON file with proper English content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Only translate title and description initially
    # Content and pros_and_cons would need more sophisticated translation

    if 'title' in data:
        data['title'] = translate_title(data['title'])

    if 'description' in data:
        data['description'] = translate_description(data['description'])

    # For now, leave content and pros_and_cons as they would need
    # proper translation API or manual translation

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return filepath

def main():
    """Process all files."""
    base_dir = Path('/Users/gejiayu/owner/seo/data/transportation-fleet-tools')

    count = 0
    for filepath in sorted(base_dir.glob('*.json')):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        title = data.get('title', '')
        language = data.get('language', '')

        if language == 'en-US' and re.search('[一-鿿]', title):
            translate_json_file(filepath)
            count += 1
            print(f"Processed: {filepath.name}")

    print(f"\nTotal files processed: {count}")

if __name__ == '__main__':
    main()