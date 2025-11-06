# Technical Design Document

## Solution Overview

The AI-Powered IT Asset Portal is an enterprise application that streamlines IT asset request management using Microsoft Power Platform and Azure AI services.

## Business Requirements

### Primary Objectives
1. Reduce manual effort in categorizing and prioritizing IT requests
2. Provide self-service portal for employees to submit and track requests
3. Enable conversational AI support through Copilot Studio
4. Automate approval workflows for high-priority requests
5. Maintain audit trail for compliance

### Success Metrics
- 80% reduction in time spent on request categorization
- 90% accuracy in AI-driven category assignment
- <30 second average response time for request submission
- 95% user satisfaction with self-service experience

## Architecture

### Component Diagram
```
┌─────────────────────────────────────────────────────────────┐
│                        End Users                             │
│  (Power Pages Portal / Copilot Studio / Power Apps)         │
└──────────────┬──────────────────────────┬───────────────────┘
               │                          │
               ▼                          ▼
      ┌────────────────┐         ┌────────────────┐
      │  Power Pages   │         │ Copilot Studio │
      │    Portal      │         │      Bot       │
      └────────┬───────┘         └────────┬───────┘
               │                          │
               │         ┌────────────────▼─────────┐
               │         │   Power Automate Flow    │
               │         │  (Business Logic Layer)  │
               │         └────────┬─────────────────┘
               │                  │
               ▼                  ▼
      ┌─────────────────────────────────┐
      │         Dataverse               │
      │      (Data Layer)               │
      │  • Asset Request Table          │
      │  • Request Comment Table        │
      └─────────────────────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Custom Connector │
              └────────┬─────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Azure Function  │
              │  (API Layer)    │
              └────────┬─────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Azure AI Foundry│
              │  with GPT-4     │
              │  (AI Service)   │
              └─────────────────┘
```

### Data Flow

1. **Request Creation**
   - User submits request via Power Pages or Copilot Studio
   - Request saved to Dataverse (Asset Request table)
   - Power Automate flow triggered

2. **AI Analysis**
   - Flow extracts request details
   - Calls Azure Function via custom connector
   - Function invokes Azure AI Foundry (Azure OpenAI) with structured prompt
   - Returns category and priority

3. **Workflow Routing**
   - Flow updates request with AI insights
   - High-priority requests (4-5) route to Teams approval
   - Low-priority requests auto-approved
   - Notifications sent to requestor

4. **Comments & Updates**
   - Users and approvers add comments (Request Comment table)
   - Status updates trigger notifications
   - Audit log maintained automatically

## Technology Choices

### Why Power Platform?
- **Rapid Development**: Low-code approach accelerates delivery
- **Native Integration**: Seamless connection between components
- **Scalability**: Microsoft cloud infrastructure
- **Governance**: Built-in ALM and compliance features

### Why Azure AI Foundry?
- **Unified Platform**: Centralized management of all Azure AI services
- **Enterprise-Grade AI**: Production-ready GPT-4 and GPT-4o models
- **Built-in Monitoring**: Real-time metrics and usage tracking
- **Data Privacy**: Data not used for model training
- **Security**: Azure AD integration and RBAC
- **Flexibility**: Easy model deployment and prompt management
- **Future-Ready**: Access to latest AI models and features (GPT-4o, etc.)

### Why Azure Functions?
- **Serverless**: No infrastructure management
- **Cost-Effective**: Pay-per-execution model
- **Scalable**: Auto-scales based on demand
- **Integration**: Easy connection to Power Platform

## Security Design

### Authentication & Authorization
- **Power Pages**: Azure AD B2C for external users
- **Copilot Studio**: Azure AD SSO
- **Azure Function**: API key + CORS restrictions
- **Dataverse**: Role-based security (IT Manager, Regular User)

### Data Protection
- **Encryption at Rest**: Dataverse built-in encryption
- **Encryption in Transit**: HTTPS only
- **Field-Level Security**: Sensitive fields (Request Details, Requestor)
- **Audit Logging**: All CRUD operations tracked

### Compliance
- **GDPR**: Right to access, delete personal data
- **Data Residency**: Dataverse environment in required geography
- **Retention Policies**: Configurable for each table

## Performance Considerations

### Expected Load
- 500 requests/day (peak: 100/hour)
- 50 concurrent users
- Average request size: 500 characters

### Optimization Strategies
- **Caching**: Azure Function output cached for 5 minutes
- **Indexing**: Dataverse columns indexed (Request Title, Status, Created On)
- **Throttling**: Rate limits on API calls (100 requests/minute)
- **Pagination**: Power Pages lists limited to 50 records per page

### SLA Targets
- **Availability**: 99.9% (Power Platform SLA)
- **Response Time**: <2 seconds for AI analysis
- **Recovery Time Objective (RTO)**: 4 hours
- **Recovery Point Objective (RPO)**: 15 minutes

## Error Handling

### Azure Function
- Input validation with clear error messages
- Retry logic for Azure AI Foundry (3 attempts, exponential backoff)
- Fallback to default values if AI fails
- Logging to Application Insights

### Power Automate
- Try-catch scope around AI connector
- Email notification on critical failures
- Automatic retry for transient errors (Azure AI Foundry throttling)
- Dead letter queue for failed requests

### User Experience
- Friendly error messages (no technical jargon)
- Fallback to manual categorization
- Support contact info displayed

## Testing Strategy

### Unit Testing
- Azure Function: pytest with mocked OpenAI responses
- Test edge cases (empty input, special characters, long text)

### Integration Testing
- End-to-end flow from Power Pages to approval
- Custom connector authentication
- Dataverse CRUD operations

### User Acceptance Testing
- 10 pilot users for 2 weeks
- Feedback collection via Power Pages form
- Iteration based on feedback

### Performance Testing
- Load testing with 100 concurrent requests
- Stress testing at 150% expected load
- Monitor Azure Function metrics

## Future Enhancements

### Phase 2 (Q1 2026)
- AI Builder integration for document analysis (upload invoices)
- Power BI dashboard for request analytics
- Mobile app with Power Apps

### Phase 3 (Q2 2026)
- Sentiment analysis on request text
- Predictive fulfillment time estimates
- Integration with ServiceNow for ticket sync

### Phase 4 (Q3 2026)
- Multi-language support with Azure Translator
- Advanced chatbot with generative answers
- Workflow automation suggestions using AI

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Azure AI Foundry service outage | High | Low | Fallback to default category/priority, monitor service health |
| Model deprecation (GPT-4) | Medium | Low | Easy migration to newer models (GPT-4o) via AI Foundry |
| Dataverse storage limits | Medium | Medium | Archive old requests quarterly |
| User adoption resistance | High | Medium | Training sessions, champions program |
| Security breach | High | Low | Regular audits, penetration testing |

## Cost Estimate

### Monthly Operating Costs
- Power Platform (per app plan): $20/user (10 users) = $200
- Azure Function (consumption): ~$5
- Azure AI Foundry with GPT-4o (pay-per-token): ~$10-30
- Azure Storage: ~$2
- **Total: ~$220-240/month**

*Note: Using GPT-4o instead of GPT-4 reduces AI costs by ~70% with similar performance*

### Development Costs (One-Time)
- Solution design: 40 hours
- Development & testing: 80 hours
- Documentation: 20 hours
- Deployment: 10 hours
- **Total: 150 hours**

## Maintenance Plan

### Weekly
- Review error logs
- Check connector health

### Monthly
- Review user feedback
- Update documentation
- Security patch assessment

### Quarterly
- Rotate API keys
- Review and optimize AI prompts
- Performance review
- Cost optimization review

---

**Document Version**: 1.0  
**Last Updated**: November 4, 2025  
**Author**: [Sankeerth Boddu]  
