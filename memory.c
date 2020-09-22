#include <linux/init.h>//init cleanup
#include <linux/kernel.h>//printk
#include <linux/module.h>//module headers
#include <linux/slab.h>//kmalloc kfree
#include <linux/fs.h>//fops
#include <linux/kdev_t.h>//mkdev
#include <linux/cdev.h>//cdev
#include <linux/uaccess.h>//copy user kernel
#include <linux/types.h>//kernel predefined detatypes
#include<linux/version.h>
#include <linux/errno.h> /* error codes */
#include <linux/fcntl.h> /* O_ACCMODE */
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("This is my test module of character driver");

dev_t chr_dev;
struct cdev my_cdev;
static struct class *dev_class;
char *memory_buffer;
#define memsize 120
ssize_t my_read(struct file *filp,char __user *Ubuff,size_t count,loff_t *offp);
ssize_t my_write(struct file *filp,const char __user *Ubuff,size_t count,loff_t *offp);
int my_open(struct inode *inode,struct file *filp);
int my_release(struct inode *inode,struct file *filp);

struct file_operations fops=
{
	.owner = THIS_MODULE,
	.read  = my_read,
	.write = my_write,
	.open  = my_open,
	.release = my_release,
};
//init module
static int __init chr_init(void)
{
	/*allocating major number*/
	if(alloc_chrdev_region(&chr_dev,0,1,"mydev")<0)
	{
		printk(KERN_INFO"can not allocate major number");
	}

	printk("\nThe Major Number is %d...THe Minor Number is %d\n",MAJOR(chr_dev),MINOR(chr_dev));

	/*class create*/
	if((dev_class=class_create(THIS_MODULE,"myclass"))==NULL)
        {
                printk(KERN_INFO"class not created\n");
                goto r_class;
        }
	/*create device*/
	if(device_create(dev_class,NULL,chr_dev,NULL,"mydev")==NULL)
        {
                printk(KERN_INFO"device not created\n");
                goto r_device;
        }

	/*create cdev structure*/
        cdev_init(&my_cdev,&fops);
        /*adding character device to system*/
        if(cdev_add(&my_cdev,chr_dev,1)<0)
        {
                printk(KERN_INFO"can not add to system\n");
                goto r_cdev;
        }
  memory_buffer = kmalloc(memsize, GFP_KERNEL);
  memset(memory_buffer, 0, 1);
  printk("Inserting module\n");
	return 0;
r_cdev:
	device_destroy(dev_class,chr_dev);
r_device:
	class_destroy(dev_class);
r_class:
	 unregister_chrdev_region(chr_dev,1);
	 return -1;
}
//clean up module
static void __exit chr_exit(void)
{
	cdev_del(&my_cdev);
	device_destroy(dev_class,chr_dev);
	class_destroy(dev_class);
	unregister_chrdev_region(chr_dev,1);
	if (memory_buffer)
	{
	       	kfree(memory_buffer);
 	}
	printk(KERN_INFO "I have unregistered the stuff that was allocated.....Goodbye for ever.....\n");
}
int  my_open(struct inode *inode,struct file *filp)
{
	printk(KERN_INFO "\nThis is the Kernel....Open Call\n");
        return 0;
}
int my_release(struct inode *inode,struct file *filp)
{
	printk(KERN_INFO "\nThis is the release method of my Character Driver\n");
        return 0;	
}
ssize_t my_read(struct file *filp,char __user *Ubuff,size_t count,loff_t *offp)
{
        int result;
        ssize_t retval;

        result=copy_to_user(Ubuff,memory_buffer,sizeof(memory_buffer));

        if(result == 0)
        {
                printk(KERN_INFO"copy to user space is successfully written %ld\n",sizeof(memory_buffer));
                retval = sizeof(memory_buffer);
                if (*offp == 0)
                {
                *offp = retval;
                return retval;
                }
                else
                return 0;
        }
        else
        {
                printk(KERN_INFO"\n Error Writing Data to User\n");
                retval=-EFAULT;
                return retval;
        }
}
ssize_t my_write(struct file *filp, const char __user *Ubuff,size_t count,loff_t *offp)
{
        int result;
        ssize_t retval;

        result=copy_from_user(memory_buffer,Ubuff,count);
        if(result == 0)
        {
                printk(KERN_INFO "\nMessage from the user......\n %s\n",memory_buffer);
                printk(KERN_INFO "\n %ld bytes of data Successfully Written.....\n",count);
                retval=count;
                return retval;

        }
        else
        {
                printk(KERN_INFO "\n Error Writing Data\n");
                retval=-EFAULT;
                return retval;

        }
        
}
module_init(chr_init);
module_exit(chr_exit);
