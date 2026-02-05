# Code-to-Diagram Patterns

Maps code constructs to diagram elements across different languages.

## Table of Contents

1. [Language-Agnostic Patterns](#language-agnostic-patterns)
2. [Python Patterns](#python-patterns)
3. [TypeScript/JavaScript Patterns](#typescriptjavascript-patterns)
4. [Java/C# Patterns](#javac-patterns)
5. [Database/SQL Patterns](#databasesql-patterns)
6. [API Patterns](#api-patterns)

---

## Language-Agnostic Patterns

### Control Flow → Flow Diagram

| Code Construct | Diagram Element |
|----------------|-----------------|
| `if/else` | Diamond decision with Yes/No branches |
| `switch/case` | Diamond with multiple outgoing arrows |
| `for/while` loop | Process box with loop-back arrow |
| `try/catch` | Process box with error path (red arrow) |
| Function call | Arrow to called function box |
| Return | Arrow back to caller (dashed) |

### OOP → Class Diagram

| Code Construct | Diagram Element |
|----------------|-----------------|
| Class definition | Rectangle with 3 sections |
| Interface/Protocol | Rectangle with <<interface>> |
| Abstract class | Rectangle with <<abstract>> |
| `extends`/inheritance | Solid arrow with triangle head |
| `implements` | Dashed arrow with triangle head |
| Composition (has-a, lifetime) | Filled diamond at owner |
| Aggregation (has-a, shared) | Empty diamond at owner |
| Association (uses) | Simple arrow |
| Public member | `+ name` |
| Private member | `- name` |
| Protected member | `# name` |
| Static member | Underlined |

### Data Structures → ER Diagram

| Code Construct | Diagram Element |
|----------------|-----------------|
| Model/Entity class | Entity box |
| Primary key field | 🔑 or PK marker |
| Foreign key field | FK marker with relationship line |
| One-to-one | `1 — 1` line |
| One-to-many | `1 — *` line |
| Many-to-many | `* — *` line (usually junction table) |

---

## Python Patterns

### Class Definition

```python
class UserService:
    def __init__(self, db: Database):
        self._db = db
        self.cache = {}
    
    def get_user(self, id: str) -> User:
        pass
    
    def _validate(self, data: dict) -> bool:
        pass
```

**Maps to:**
```
┌─────────────────────────┐
│      UserService        │
├─────────────────────────┤
│ - _db: Database         │
│ + cache: dict           │
├─────────────────────────┤
│ + get_user(id): User    │
│ - _validate(data): bool │
└─────────────────────────┘
```

### Inheritance

```python
class Animal(ABC):
    @abstractmethod
    def speak(self): pass

class Dog(Animal):
    def speak(self):
        return "woof"
```

**Maps to:**
```
┌───────────────┐
│ <<abstract>>  │
│    Animal     │
├───────────────┤
│ + speak()*    │
└───────────────┘
        △
        │ (inheritance)
        │
┌───────────────┐
│     Dog       │
├───────────────┤
│ + speak()     │
└───────────────┘
```

### Dataclass → ER Entity

```python
@dataclass
class User:
    id: int  # primary key
    email: str
    profile_id: int  # foreign key
    created_at: datetime
```

**Maps to:**
```
┌─────────────────┐
│      USER       │
├─────────────────┤
│ 🔑 id           │
│    email        │
│ FK profile_id   │
│    created_at   │
└─────────────────┘
```

### Function Flow

```python
def process_order(order):
    if not validate(order):
        raise ValidationError()
    
    total = calculate_total(order)
    
    if total > 1000:
        apply_discount(order)
    
    save_order(order)
    return order.id
```

**Maps to flow diagram:**
```
    (Start)
        │
        ▼
   ┌─────────┐
   │validate │
   └────┬────┘
        │
    ◇ valid?
   /         \
  No          Yes
  │            │
  ▼            ▼
[Error]   ┌─────────────┐
          │calc_total   │
          └──────┬──────┘
                 │
             ◇ >1000?
            /       \
           Yes       No
           │         │
           ▼         │
    ┌───────────┐    │
    │ discount  │    │
    └─────┬─────┘    │
          └────┬─────┘
               │
               ▼
        ┌───────────┐
        │save_order │
        └─────┬─────┘
              │
              ▼
           (End)
```

---

## TypeScript/JavaScript Patterns

### Interface + Implementation

```typescript
interface AuthProvider {
    authenticate(creds: Credentials): Promise<Token>;
    validate(token: Token): boolean;
}

class JWTProvider implements AuthProvider {
    private secret: string;
    
    authenticate(creds: Credentials): Promise<Token> { ... }
    validate(token: Token): boolean { ... }
}
```

**Maps to class diagram with dashed implementation arrow.**

### React Component → Component Diagram

```typescript
// AuthForm.tsx
import { useAuth } from './hooks/useAuth';
import { validateEmail } from './utils/validation';

export const AuthForm: React.FC = () => {
    const { login } = useAuth();
    // ...
}
```

**Maps to:**
```
┌──┬────────────────┐
│  │   AuthForm     │
│──┤                │
│  │                │
├──○ useAuth        │ (required interface)
│                   │
╞══( validateEmail  │ (required interface)
└───────────────────┘
```

### Async Flow

```typescript
async function fetchUserData(userId: string) {
    try {
        const user = await api.getUser(userId);
        const posts = await api.getUserPosts(userId);
        return { user, posts };
    } catch (error) {
        logger.error(error);
        throw new FetchError(error);
    }
}
```

**Maps to sequence diagram:**
```
Client          API           Logger
  │              │              │
  │──getUser────>│              │
  │<─────────────│              │
  │              │              │
  │──getPosts───>│              │
  │<─────────────│              │
  │              │              │
  │ (on error)   │              │
  │──────────────┼─────error───>│
  │              │              │
```

---

## Java/C# Patterns

### Generics

```java
public interface Repository<T, ID> {
    T findById(ID id);
    List<T> findAll();
    void save(T entity);
}

public class UserRepository implements Repository<User, Long> {
    // implementation
}
```

**Maps to:**
```
┌──────────────────────────┐
│     <<interface>>        │
│   Repository<T, ID>      │
├──────────────────────────┤
│ + findById(ID): T        │
│ + findAll(): List<T>     │
│ + save(T): void          │
└──────────────────────────┘
            △
            ┆ (implements)
            ┆
┌──────────────────────────┐
│    UserRepository        │
│  «binds T=User, ID=Long» │
├──────────────────────────┤
│ + findById(Long): User   │
│ + findAll(): List<User>  │
│ + save(User): void       │
└──────────────────────────┘
```

### Dependency Injection

```csharp
public class OrderService {
    private readonly IOrderRepository _repo;
    private readonly IPaymentGateway _payment;
    
    public OrderService(IOrderRepository repo, IPaymentGateway payment) {
        _repo = repo;
        _payment = payment;
    }
}
```

**Maps to class diagram with dependency arrows:**
```
┌─────────────────┐    ┌──────────────────┐
│<<interface>>    │    │  <<interface>>   │
│IOrderRepository │    │ IPaymentGateway  │
└────────△────────┘    └────────△─────────┘
         ┆                      ┆
         ┆ (dependency)         ┆
         ┆                      ┆
         └──────────┬───────────┘
                    │
            ┌───────┴───────┐
            │  OrderService │
            └───────────────┘
```

---

## Database/SQL Patterns

### Table Definition → ER Entity

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    profile_id INT REFERENCES profiles(id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    bio TEXT
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    title VARCHAR(255),
    content TEXT,
    published_at TIMESTAMP
);
```

**Maps to ER diagram:**
```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   USERS     │      │  PROFILES   │      │   POSTS     │
├─────────────┤      ├─────────────┤      ├─────────────┤
│ 🔑 id       │      │ 🔑 id       │      │ 🔑 id       │
│    email    │      │   first_name│      │ FK user_id  │
│   password  │1    1│   last_name │      │    title    │
│ FK profile──┼──────┤    bio      │      │    content  │
│   created_at│      └─────────────┘      │  published  │
└──────┬──────┘                           └─────────────┘
       │1                                        *│
       └─────────────────────────────────────────┘
            (one user has many posts)
```

### Query Flow

```sql
SELECT u.email, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id
HAVING COUNT(p.id) > 5
ORDER BY post_count DESC;
```

**Maps to flow diagram showing data transformation:**
```
┌─────────┐    ┌─────────┐
│ users   │    │ posts   │
└────┬────┘    └────┬────┘
     │              │
     └──────┬───────┘
            │
     ┌──────▼──────┐
     │  LEFT JOIN  │
     │ ON u.id=p.id│
     └──────┬──────┘
            │
     ┌──────▼──────┐
     │   WHERE     │
     │ created_at> │
     └──────┬──────┘
            │
     ┌──────▼──────┐
     │  GROUP BY   │
     │    u.id     │
     └──────┬──────┘
            │
     ┌──────▼──────┐
     │   HAVING    │
     │  COUNT > 5  │
     └──────┬──────┘
            │
     ┌──────▼──────┐
     │  ORDER BY   │
     │ post_count  │
     └──────┬──────┘
            │
         [Result]
```

---

## API Patterns

### REST Endpoints → Sequence Diagram

```python
# routes/users.py
@router.get("/users/{id}")
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(404)
    return user

@router.post("/users")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    return db_user
```

**Maps to sequence diagram:**
```
Client       Router       Handler        DB
  │            │            │            │
  │──GET /users/1──────────>│            │
  │            │            │──query────>│
  │            │            │<───────────│
  │<───────────┼────────────│            │
  │   200 OK   │            │            │
  │            │            │            │
  │──POST /users───────────>│            │
  │            │            │──insert───>│
  │            │            │──commit───>│
  │            │            │<───────────│
  │<───────────┼────────────│            │
  │  201 Created            │            │
```

### Microservices → Component Diagram

```yaml
# docker-compose.yml
services:
  api-gateway:
    depends_on: [auth-service, user-service]
  auth-service:
    depends_on: [redis]
  user-service:
    depends_on: [postgres]
  redis:
  postgres:
```

**Maps to:**
```
┌────────────────────────────────────────────────┐
│                 API Gateway                     │
├──○ IAuth    ────────────────────○ IUser ───────┤
└────────────────────────────────────────────────┘
         │                              │
         │                              │
    ┌────▼────┐                    ┌────▼────┐
    │┌──┬─────┤                    │┌──┬─────┤
    ││  │Auth │                    ││  │User │
    │└──┤Svc  │                    │└──┤Svc  │
    └────┬────┘                    └────┬────┘
         │                              │
    ┌────▼────┐                    ┌────▼────┐
    │  Redis  │                    │Postgres │
    │   🗄️    │                    │   🗄️    │
    └─────────┘                    └─────────┘
```

---

## Explanation Template

When analyzing code, structure explanations as:

```markdown
## Overview
[1-2 sentences on what the code does]

## Key Components
- **ComponentA**: [role/purpose]
- **ComponentB**: [role/purpose]

## Execution Flow
1. [First step]
2. [Second step]
3. ...

## Data Flow
[How data moves through the system]

## Design Patterns Used
- [Pattern]: [where/why used]

## Diagram
See: `{filename}.excalidraw`
```
