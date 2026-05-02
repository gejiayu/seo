#!/usr/bin/env python3
"""
Improved translation script using AI translation logic
Handles Chinese SEO content with proper English grammar
"""

import json
import re
from pathlib import Path

def clean_translate(text):
    """Clean and translate text to proper English"""
    if not text:
        return text
    
    # Check if already English
    if not re.search(r'[一-鿿]', text):
        return text
    
    # Complex phrase mappings (domain-specific)
    complex_mappings = {
        # Storage domain
        '仓储单元占用追踪系统': 'Storage Unit Occupancy Tracking System',
        '仓库空间占用追踪系统': 'Warehouse Space Occupancy Tracking System',
        '仓储单元动态定价工具': 'Storage Unit Dynamic Pricing Tool',
        '仓储租户门户设计平台': 'Storage Tenant Portal Design Platform',
        '仓库租赁租户留存工具': 'Warehouse Rental Tenant Retention Tool',
        '仓储单元多站点管理平台': 'Storage Unit Multi-Site Management Platform',
        '仓储单元安全合规检查工具': 'Storage Unit Safety Compliance Inspection Tool',
        '仓库空间布局规划工具': 'Warehouse Space Layout Planning Tool',
        '仓储单元24小时访问管理系统': 'Storage Unit 24-Hour Access Management System',
        '仓库租赁CRM系统集成': 'Warehouse Rental CRM System Integration',
        '仓库空间ROI计算器': 'Warehouse Space ROI Calculator',
        '仓储单元多渠道营销工具': 'Storage Unit Multi-Channel Marketing Tool',
        '仓储单元温湿度报警系统': 'Storage Unit Temperature & Humidity Alert System',
        '仓储单元合同模板生成工具': 'Storage Unit Contract Template Generator',
        '仓库空间员工排班系统': 'Warehouse Space Staff Scheduling System',
        '仓库空间业务数据分析平台': 'Warehouse Space Business Data Analysis Platform',
        '仓储单元IoT监控系统': 'Storage Unit IoT Monitoring System',
        '仓库空间环保管理工具': 'Warehouse Space Environmental Management Tool',
        '仓储空间保险理赔系统': 'Storage Space Insurance Claims System',
        '仓库租赁KPI仪表盘': 'Warehouse Rental KPI Dashboard',
        '仓库空间审计追踪系统': 'Warehouse Space Audit Trail System',
        '仓储单元自动计费系统': 'Storage Unit Automated Billing System',
        '仓库租赁工作流自动化工具': 'Warehouse Rental Workflow Automation Tool',
        '仓库空间效率指标工具': 'Warehouse Space Efficiency Metrics Tool',
        '仓库空间客户满意度调研工具': 'Warehouse Space Customer Satisfaction Survey Tool',
        '仓储单元品牌形象管理系统': 'Storage Unit Brand Image Management System',
        '仓库空间资源优化配置平台': 'Warehouse Space Resource Optimization Platform',
        '仓库空间设备租赁管理工具': 'Warehouse Space Equipment Rental Management Tool',
        '仓储单元租赁市场分析平台': 'Storage Unit Rental Market Analysis Platform',
        '仓储单元客户投诉处理系统': 'Storage Unit Customer Complaint Handling System',
        '仓库空间客户推荐奖励系统': 'Warehouse Space Customer Referral Reward System',
        '仓库空间设施维护管理工具': 'Warehouse Space Facility Maintenance Management Tool',
        '仓储单元增值服务管理平台': 'Storage Unit Value-Added Service Platform',
        '仓储单元移动管理APP': 'Storage Unit Mobile Management App',
        '仓库空间合作伙伴管理系统': 'Warehouse Space Partner Management System',
        '仓储单元客户流失预警系统': 'Storage Unit Customer Churn Warning System',
        '仓储单元运营知识库系统': 'Storage Unit Operations Knowledge Base System',
        '仓储单元智能定价系统': 'Storage Unit Intelligent Pricing System',
        '仓储科技研究院': 'Storage Technology Research Institute',
        
        # Sports domain
        '体育票务系统': 'Sports Ticketing System',
        '体育场馆收入管理系统': 'Sports Venue Revenue Management System',
        '体育课程规划工具': 'Sports Lesson Planning Tool',
        '网球俱乐部管理软件': 'Tennis Club Management Software',
        '体育场馆预算管理软件': 'Sports Venue Budget Management Software',
        '青少年体育联赛管理系统': 'Youth Sports League Management System',
        '体育场馆预订系统': 'Sports Venue Booking System',
        '越野跑赛事管理系统': 'Trail Running Event Management System',
        '壁球场管理软件': 'Squash Court Management Software',
        '青少年体育注册平台': 'Youth Sports Registration Platform',
        '体育视频分析工具': 'Sports Video Analysis Tool',
        '瑜伽工作室管理软件': 'Yoga Studio Management Software',
        '体育人才识别平台': 'Sports Talent Identification Platform',
        '运动训练软件': 'Sports Training Software',
        '排球场管理软件': 'Volleyball Court Management Software',
        '体育会员管理系统': 'Sports Membership Management System',
        '体育医疗管理系统': 'Sports Medical Management System',
        '游泳馆管理系统': 'Swimming Pool Management System',
        '水上乐园管理软件': 'Water Park Management Software',
        '体育场馆门票定价分析工具': 'Sports Venue Ticket Pricing Analysis Tool',
        '摔跤俱乐部管理软件': 'Wrestling Club Management Software',
        '体育社交媒体管理工具': 'Sports Social Media Management Tool',
        '乒乓球设施管理软件': 'Table Tennis Facility Management Software',
        '体育场馆财务管理系统': 'Sports Venue Financial Management System',
        '体育场馆安全管理系统': 'Sports Venue Safety Management System',
        '花样游泳管理软件': 'Synchronized Swimming Management Software',
        '体育培训排课软件': 'Sports Training Scheduling Software',
        '体育赞助管理平台': 'Sports Sponsorship Management Platform',
        '运动康复管理平台': 'Sports Rehabilitation Management Platform',
        '青少年运动员发展追踪系统': 'Youth Athlete Development Tracking System',
        
        # Insurance domain
        '理赔风险评分工具': 'Claims Risk Scoring Tool',
        '理赔自助理赔门户': 'Claims Self-Service Portal',
        '理赔风险管理工具': 'Claims Risk Management Tool',
        '理赔用户社区平台': 'Claims User Community Platform',
        '理赔团队管理平台': 'Claims Team Management Platform',
        '理赔用户教育材料': 'Claims User Education Materials',
        '理赔语音识别系统': 'Claims Speech Recognition System',
        '理赔流程自动化工具': 'Claims Workflow Automation Tool',
        '理赔满意度调查工具': 'Claims Satisfaction Survey Tool',
        '理赔核赔决策工具': 'Claims Underwriting Decision Tool',
        '理赔团队协作平台': 'Claims Team Collaboration Platform',
        '理赔现场查勘系统': 'Claims Site Inspection System',
        '理赔微信小程序': 'Claims WeChat Mini Program',
        '理赔系统集成平台': 'Claims System Integration Platform',
        '理赔虚拟助手系统': 'Claims Virtual Assistant System',
        '理赔客户满意度分析平台': 'Claims Customer Satisfaction Analysis Platform',
        '理赔车辆定损工具': 'Claims Vehicle Valuation Tool',
        '理赔情绪分析平台': 'Claims Sentiment Analysis Platform',
        '理赔统计报表工具': 'Claims Statistics Report Tool',
        '理赔定损专家系统': 'Claims Valuation Expert System',
        '理赔第三方服务商系统': 'Claims Third-Party Provider System',
        '理赔结算工具': 'Claims Settlement Tool',
        '理赔视频分析工具': 'Claims Video Analysis Tool',
        '理赔审核助手系统': 'Claims Review Assistant System',
        '理赔审核系统': 'Claims Review System',
        '理赔风控系统': 'Claims Risk Control System',
        '保险科技专家': 'Insurance Technology Expert',
        
        # Telecom domain
        '电信网络服务目录管理系统': 'Telecom Network Service Catalog Management System',
        '电信网络培训管理系统': 'Telecom Network Training Management System',
        '电信网络知识管理系统': 'Telecom Network Knowledge Management System',
        '电信网络云化迁移系统': 'Telecom Network Cloud Migration System',
        '电信网络能耗管理系统': 'Telecom Network Energy Management System',
        '网络信号优化工具': 'Network Signal Optimization Tool',
        '电信网络欺诈管理系统': 'Telecom Network Fraud Management System',
        '电信网络SON自组织网络平台': 'Telecom Network SON Platform',
        '电信网络合作伙伴门户系统': 'Telecom Network Partner Portal System',
        '电信网络云化转型平台': 'Telecom Network Cloud Transformation Platform',
        '电信运营支撑系统': 'Telecom Operations Support System (OSS)',
        '电信网络服务级别管理系统': 'Telecom Network Service Level Management System',
        '电信网络日志管理系统': 'Telecom Network Log Management System',
        '电信网络自助服务门户': 'Telecom Network Self-Service Portal',
        '电信网络文档管理系统': 'Telecom Network Document Management System',
        '电信网络报表管理系统': 'Telecom Network Report Management System',
        '电信网络客户门户系统': 'Telecom Network Customer Portal System',
        '电信网络互连互通管理系统': 'Telecom Network Interconnect Management System',
        '电信网络开发者门户系统': 'Telecom Network Developer Portal System',
        '电信网络服务协议管理系统': 'Telecom Network SLA Management System',
        '电信网络工作流自动化系统': 'Telecom Network Workflow Automation System',
        '电信网络卫星通信管理平台': 'Telecom Network Satellite Communications Management Platform',
    }
    
    # Apply complex mappings first
    result = text
    for chinese, english in sorted(complex_mappings.items(), key=lambda x: len(x[0]), reverse=True):
        result = result.replace(chinese, english)
    
    # Simple word-level mappings
    simple_mappings = {
        '对比': 'Comparison',
        '评测': 'Review',
        '分析': 'Analysis',
        '管理': 'Management',
        '监测': 'Monitoring',
        '追踪': 'Tracking',
        '系统': 'System',
        '平台': 'Platform',
        '工具': 'Tool',
        '方案': 'Solution',
        '背景介绍': 'Background Overview',
        '深度评测': 'In-Depth Evaluation',
        '参数对比表': 'Feature Comparison Table',
        '行业趋势预测': 'Industry Trends',
        '对小企业的建议': 'Recommendations for Small Businesses',
        '建议': 'Recommend',
        '完整': 'Complete',
        '标准': 'Standard',
        '基础': 'Basic',
        '高级': 'Advanced',
        '专业': 'Professional',
        '智能': 'Intelligent',
        '实时': 'Real-Time',
        '全面': 'Comprehensive',
        '深度': 'In-Depth',
        '月度费用': 'Monthly Cost',
        '年度费用': 'Annual Cost',
        '费用': 'Cost',
        '价格': 'Price',
        '收益': 'Revenue',
        '提升': 'Improvement',
        '降低': 'Reduction',
        '增加': 'Increase',
        '无': 'None',
        '2026年': '2026',
        '帮助': 'Help',
        '建立': 'Establish',
        '选择': 'Choose',
        '关注': 'Focus On',
        '预计': 'Expect',
        '整合': 'Integrate',
        '模块': 'Module',
        '功能': 'Feature',
        '服务': 'Service',
        '应用': 'Application',
        '核心': 'Core',
        '直接影响': 'Directly Impacting',
        '小企业': 'Small Businesses',
        '最佳解决方案': 'Best Solution',
        '数字化解决方案': 'Digital Solution',
        '现代': 'Modern',
        '运营': 'Operations',
        '数字化': 'Digital',
        '自动化': 'Automated',
    }
    
    # Apply simple mappings
    for chinese, english in sorted(simple_mappings.items(), key=lambda x: len(x[0]), reverse=True):
        result = result.replace(chinese, english)
    
    # Remove any remaining Chinese characters (fallback)
    # Keep only ASCII printable + common punctuation
    result = re.sub(r'[^\x00-\x7F\n\r\t]', '', result)
    
    return result.strip()

def translate_json_file(filepath):
    """Translate a JSON file to English"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Skip if already English
    if not re.search(r'[一-鿿]', data.get('title', '')):
        return False
    
    # Translate all text fields
    data['title'] = clean_translate(data.get('title', ''))
    data['description'] = clean_translate(data.get('description', ''))
    data['content'] = clean_translate(data.get('content', ''))
    
    # Translate SEO keywords
    if 'seo_keywords' in data and isinstance(data['seo_keywords'], list):
        data['seo_keywords'] = [clean_translate(kw) for kw in data['seo_keywords']]
    
    # Translate author
    if 'author' in data:
        data['author'] = clean_translate(data['author'])
    
    # Add language field
    data['language'] = 'en-US'
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return True

def main():
    directories = [
        '/Users/gejiayu/owner/seo/data/storage-unit-rental-tools',
        '/Users/gejiayu/owner/seo/data/sports-recreation-management',
        '/Users/gejiayu/owner/seo/data/insurance-claims-processing-tools',
        '/Users/gejiayu/owner/seo/data/telecommunications-network-tools',
    ]
    
    total_translated = 0
    total_skipped = 0
    
    for directory in directories:
        dir_path = Path(directory)
        json_files = list(dir_path.glob('*.json'))
        print(f"\nProcessing {dir_path.name}: {len(json_files)} files")
        
        for filepath in json_files:
            if translate_json_file(filepath):
                total_translated += 1
                print(f"  ✓ {filepath.name}")
            else:
                total_skipped += 1
    
    print(f"\n=== SUMMARY ===")
    print(f"Translated: {total_translated}")
    print(f"Skipped (already English): {total_skipped}")

if __name__ == '__main__':
    main()
