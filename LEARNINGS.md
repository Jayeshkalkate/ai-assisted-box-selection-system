# What I Learned

Write this section yourself after completing and testing the assignment.

The assignment specifically asks for your own answer, so do not replace this with AI-generated text.

Useful points to reflect on:

# What I Learned

This assignment did not introduce me to Python or Django from scratch, as I have already worked with Django, REST APIs, PostgreSQL, testing, Git, and deployment in my previous projects. Instead, it gave me an opportunity to apply those existing skills to a different problem involving 3D box selection and packing.

### 1. Applying algorithmic thinking to a practical backend problem

The main learning from this assignment was translating a physical packing problem into a backend algorithm. Selecting a box cannot be based only on total volume. The dimensions of individual products, their orientation, available space, weight limits, and product placement all affect whether the order can actually fit.

### 2. Handling product rotation and placement

I worked with different orientations of products while checking whether they could fit inside a box. This made me think more carefully about how dimensions should be represented and how placement decisions affect the remaining available space.

### 3. Keeping business logic separate from the Django layer

I kept the core packing logic independent from Django views and API handling. This makes the algorithm easier to test, reason about, and modify without coupling the business logic to the web framework.

### 4. Writing tests for edge cases

I already had experience with automated testing, but this assignment reinforced the importance of testing edge cases in algorithmic code. Cases such as oversized products, weight limits, multiple products, rotations, and invalid inputs are important because the normal path alone does not prove that the solution is reliable.

### 5. Using AI as a development aid rather than treating its output as final

I used AI tools during development, but I still had to review the generated suggestions, modify parts of the implementation, identify mistakes, and verify the final behavior through tests and manual checks. This reinforced that AI can accelerate development, but the developer still needs to understand and validate the resulting code.

### 6. Verifying behavior at more than one level

Testing the packing function alone is not enough for a Django application. I also needed to verify the API behavior, validation, response structure, and integration between the application components.

### 7. Understanding the limitations of heuristic solutions

The packing problem can become computationally difficult as the number of products and possible arrangements increases. For this assignment, a practical heuristic approach is more appropriate than trying to exhaustively search every possible arrangement. This also made me more aware of the trade-off between solution quality, complexity, and execution time.

### 8. Importance of reproducible development

The assignment also reinforced the value of keeping the project reproducible through requirements management, automated tests, Git, and CI. A solution is more useful when another developer can clone the repository, install the dependencies, run the tests, and verify the result consistently.
