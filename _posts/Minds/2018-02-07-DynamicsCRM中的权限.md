# Dynamics CRM中的权限
- 1.每个实体有 创建/读/写/删除/追加/追加到/分派/共享 权限。
- 2.每个实体的每种权限深度有 用户/业务部门/业务部门及以下/整个组织 的权限。
关于迷惑了很久的追加和追加到的权限，这里有一篇文章，详细叙述

[Microsoft Dynamics CRM: Append Vs. Append To – What’s the Difference?](https://blogs.msdn.microsoft.com/crm/2009/11/18/microsoft-dynamics-crm-append-vs-append-to-whats-the-difference/)

摘录原文内容如下：
```
This post is CRM security 101, but I get asked this question fairly often, so it seems that there is some confusion about what the difference is between “Append” and “Append To” security permissions.  I find this confusion comes from the similar sounding names of these permissions, and also because configuration of relationship security requires permissions to be applied to two separate entities—both sides of the relationship.


Let’s take the example of Accounts and Opportunities.  In this relationship, “Accounts” is the parent and “Opportunities” is the child.  There are multiple Opportunities per Account.  Say a user needs to be able to relate Opportunities to Accounts, either through the Potential Customer lookup field on the Opportunity, or through the “Opportunities” navigation bar area on an account.


In this example, a user must have “Append” permissions on Opportunities (child) and “Append To” permissions on Accounts (parent).  I think of it this way—I’m APPENDING the opportunity, and I’m APPENDING it TO the account.


The next consideration is what permission level the users should have.  As with other permissions in Dynamics CRM, you can grant a role “User,” “Business Unit,” “Parent/Child Business Unit,” and “Organization” level security permissions for both append and append to.  It is important to think through what records a user should be able to append, and to which records that user should be able to append those records.


In our example of Accounts and Opportunities, if a user should be able to associate any Opportunity with any Account, you would give that user’s role Organization level Append permissions on Opportunities and Organization level Append To permissions on Accounts.  Easy enough.  What if you want to give a user permission to associate only opportunities that they own to any account in their business unit?  In this case you would give that user’s security role “User” level Append permissions on Opportunities and “Business Unit” level Append To permissions on Accounts.


Now that you have the relationship permissions set, there is one more wrinkle you need to consider.  If you want a user to be able to create related records from a parent, the user needs to have write permissions for the parent entity.  For example, if you want a user to click the Opportunities navigation bar link from an Account and create a related opportunity, that user’s security role will need to have write permission for Accounts.  If they don’t, the “new” button won’t be available from the Account.  They would be able to go to the Opportunities entity and create a new opportunity and relate it to the Account, but without write permissions on Accounts they will not be able to create related records from an Account.
```