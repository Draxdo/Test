# Semble Programming Language

Have you ever wanted something with *easy* syntax that is as *fast*¹ as C?

Well, look no further than Semble or SembleLang.

Semble is a low-level, fast, easy-to-learn, general-purpose programming language that compiles right to AT&T syntax x86² Assembly!

With libc built-in don't worry about losing all that precious knowledge you have built up about `scanf()` this and `strcat()` that. As for beginner's, Semble comes with another stdlib that builds on top on libc to provide easy-to-use functions for all sorts of things!

## Coding in semble

#### Variable declaration:

```rust
fn main => {
  let x = 6;
  let y = "Hello World!";
  let z = 'a';
  let a = true;
  let b = 0x0f;
  let c = @x;
  let d = $c;
}
```

#### Functions

```rust
fn name => {
  // code
  let y = name();
}
```

#### Pointers



### Footnotes

- 1 - you usually dont see easy and fast put together!
- 2 - yes, it is 32-bit.