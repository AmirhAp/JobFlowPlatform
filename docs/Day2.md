Job Post : 
    User Flow: what user can do : 
        - see all job postings 
        - see one job post
        - see all jobs from one company 
        - see all job posts based on its Status

        - create one new job post for a company
        
        - change status of one job post
        - edit info of one job post
        
        - remove one job post
        
        
    endpoints: 
        - GET   /posts
        - GET   /posts/{post_id}
        - GET   /companies/{company_id}/posts
        - GET   /posts?status=applied

        - POST  /posts

        - PATCH /posts/{post_id}/status
        - PUT   /posts/{post_id}

        - DELETE /posts/{post_id}
        
    Enum : 
        - Status:
            - To Review
            - Applied 
            - Rejected
            - interview
            - offered
            - closed

    schema: 
        - PostBase: 
            - title 
            - company id
            - status
        
        - PostRead:

        
    