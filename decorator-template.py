from typing import Callable


class _Decorator:
    def __init__(self, decorated_func: Callable, *decorator_args, **decorator_kwargs):
        self.decorated_func = decorated_func
        self.decorator_args = decorator_args
        self.decorator_kwargs = decorator_kwargs
        
    def __call__(self, *func_args, **func_kwargs):
        print('enter')
        print(self.decorator_args, self.decorator_kwargs)
        result = self.decorated_func(*func_args, **func_kwargs)
        print('exit')
        return result

    @classmethod
    def decorator(cls, *decorator_args, **decorator_kwargs):
        if len(decorator_args) == 1 and decorator_kwargs == {} and callable(decorator_args[0]):
            # @decorator is called
            # decorator_args[0] is the decorated func
            return cls(decorator_args[0])
        # @decorator(...) is called
        return lambda decorated_func: cls(decorated_func, *decorator_args, **decorator_kwargs)


decorator = _Decorator.decorator


class _AsyncDecorator(_Decorator):
    async def __call__(self, *func_args, **func_kwargs):
        print('async enter')
        print(self.decorator_args, self.decorator_kwargs)
        result = await self.decorated_func(*func_args, **func_kwargs)
        print('async exit')
        return result


async_decorator = _AsyncDecorator.decorator


if __name__ == '__main__':
    print('sync usage')
    
    @decorator(1, tries=1, backoff=2)
    def do_something(*args, **kwargs):
        print(args, kwargs)
    
    
    @decorator()
    def do_something_without_decorator_args(*args, **kwargs):
        print(args, kwargs)
    
    
    @decorator
    def do_something_without_decorator_call(*args, **kwargs):
        print(args, kwargs)
    
    
    do_something(1, 2, a=3, decorator_called_with='args')
    do_something_without_decorator_args(4, 5, content='content', decorator_called='without args')
    do_something_without_decorator_call(5, 6, without='decorator-call')

    print()
    print('###################################################')
    print('async usage')
    import asyncio

    @async_decorator(1, tries=1, backoff=2)
    async def do_something(*args, **kwargs):
        print(args, kwargs)


    @async_decorator()
    async def do_something_without_decorator_args(*args, **kwargs):
        print(args, kwargs)


    @async_decorator
    async def do_something_without_decorator_call(*args, **kwargs):
        print(args, kwargs)


    asyncio.run(do_something(1, 2, a=3, decorator_called_with='args'))
    asyncio.run(do_something_without_decorator_args(4, 5, content='content', decorator_called='without args'))
    asyncio.run(do_something_without_decorator_call(5, 6, without='decorator-call'))
